import os
from astral.sun import sun
from astral import LocationInfo
import numpy as np
from pytz import timezone
from datetime import datetime, timedelta

def get_weather(path, freq):
    import numpy as np
    from sklearn.preprocessing import MultiLabelBinarizer
    if isinstance(path, list):
        df = pd.DataFrame()
        for p in path:
            df = pd.concat([df, pd.read_csv(p)], ignore_index=True)
    else:
        df = pd.read_csv(path)
    
    #rename columns explicitly to match expected format
    df.columns = ['city', 'time', 'max_temp', 'min_temp', 'temp', 'wind_chill', 'heat_index',
                  'precip', 'snow', 'snow_depth', 'wind_speed', 'wind_direction', 'wind_gust',
                  'visibility', 'cloud_cover', 'humid', 'conditions']

    df = df.drop('city',axis = 1)
    #convert 'time' column to datetime with the corrected format
    df['time'] = pd.to_datetime(df['time'], format='%m/%d/%Y %H:%M:%S')
    
    #replace all NaNs with zero
    df.fillna(0, inplace=True)
    
    #one-hot encoding the 'conditions' column
    if 'conditions' in df.columns:
        df['conditions'] = df['conditions'].astype(str).replace('0', 'None').str.split(', ').apply(lambda x: [item.strip() + '_cond' for item in x])
        mlb = MultiLabelBinarizer()
        conditions_encoded = mlb.fit_transform(df['conditions'])
        new_columns = [label.lower().replace(', ', '_').replace(' ', '_') for label in mlb.classes_]
        conditions_df = pd.DataFrame(conditions_encoded, columns=new_columns, index=df.index)
        df = pd.concat([df.drop('conditions', axis=1), conditions_df], axis=1)
    
    #drop duplicate times
    df = df.drop_duplicates(subset='time', keep='first')
    
    boole, liste = check_time_increments(df,'time',df['time'].min(),df['time'].max())
    
    if not boole:
        cols = ['max_temp', 'min_temp', 'temp', 'wind_chill', 'heat_index',
                'precip', 'snow', 'snow_depth', 'wind_speed', 'wind_direction',
                'wind_gust', 'visibility', 'cloud_cover', 'humid', 'clear_cond',
                'none_cond', 'overcast_cond', 'partially_cloudy_cond', 'rain_cond',
                'snow_cond']
        
        #prepare a DataFrame with the missing times
        missing_data = pd.DataFrame({
            'time': liste,
            **{col: 0 if col != 'none_cond' else 1 for col in cols}  # Setting none_cond to 1, others to 0
        })

    #concatenate the missing data to the original DataFrame
    df = pd.concat([df, missing_data])
    df = df.sort_values('time')
    
    #keep fixing bad rows
    df = replace_rows_based_on_condition(df)
    df = replace_rows_based_on_temp(df)
    
    #encoding time
    encoded_time = df['time'].apply(lambda x: encode_cyclic(x)).apply(pd.Series)
    
    #encoding sun variables
    ecs = apply_sun(encoded_time)
    
    df = pd.merge(df, ecs, on='time', how='left')

    # Handling different frequencies
    if freq == 15:
        pass  # Data is already assumed to be in 15-minute intervals
    elif freq == 60:
        # Resample data to 1-hour intervals
        df = df.set_index('time')
        df = df.resample('1H').mean().reset_index()
        for nc in new_columns:
            df[nc] = np.where(df[nc] > 0, 1, 0)
    return df

def encode_cyclic(datetime_obj):
    max_dict = {'month': 12, 'day': 31, 'hour': 24, 'minute': 60, 'day_of_week': 7}
    ll = {}
    ll['time'] = datetime_obj
    for component_name, max_value in max_dict.items():
        if component_name == 'minute':
            component_name = 'minute'  # Adjust for naming consistency
        if component_name == 'day_of_week':
            component_value = datetime_obj.weekday()  # Use weekday() for day of the week
        else:
            component_value = getattr(datetime_obj, component_name)
        sin_encoded = np.sin(2 * np.pi * component_value / max_value)
        cos_encoded = np.cos(2 * np.pi * component_value / max_value)
        ll[component_name + '_sin'] = sin_encoded
        ll[component_name + '_cos'] = cos_encoded
    return ll

def load_astral():
    city_name = "New York"
    country = "USA"
    latitude = 40.7128
    longitude = -74.0060
    return LocationInfo(city_name, country, timezone='UTC', latitude=latitude, longitude=longitude)
    

def get_sun(day, month, year, city):
    try:
        s = sun(city.observer, date=datetime(year, month, day))
    except ValueError as e:
        # If no sunrise/sunset times are found for the specified date, try the next day
        next_day = datetime(year, month, day) + timedelta(days=1)
        s = sun(city.observer, date=next_day)
    
    # Define NYC timezone
    nyc_tz = timezone('America/New_York')
    
    # Convert sunrise and sunset times to NYC time
    sun_times = {key: s[key].astimezone(nyc_tz).strftime('%Y-%m-%d %H:%M:%S') for key in s.keys()}
    
    
    return sun_times

def apply_sun(df):
    #define NYC timezone
    nyc_tz = timezone('America/New_York')
    
    sun_cache = {}
    
    #check if columns exist, otherwise create them
    if 'dark' not in df.columns:
        df['dark'] = 0
    if 'part_dark' not in df.columns:
        df['part_dark'] = 0
    if 'light' not in df.columns:
        df['light'] = 0
    
    #load location information
    city = load_astral()
    
    #iterate each row in the df
    for index, row in df.iterrows():
        timestamp = pd.to_datetime(row['time'])  #ensure timestamp is in datetime format

        year = timestamp.year
        month = timestamp.month
        day = timestamp.day

        #check if sun times for this day are already cached
        if (year, month, day) not in sun_cache:
            
            sun_times = get_sun(day, month, year, city)
            #logging.log(sun_times)

            #gotta cache 'em all 
            sun_cache[(year, month, day)] = sun_times

        #retrieve sunrise and sunset times from cache
        cached_sun_times = sun_cache[(year, month, day)]

        #convert cached sunrise, sunset, dawn, and dusk to datetime objects
        sunrise = pd.to_datetime(cached_sun_times['sunrise'])
        sunset = pd.to_datetime(cached_sun_times['sunset'])
        dawn = pd.to_datetime(cached_sun_times['dawn'])
        dusk = pd.to_datetime(cached_sun_times['dusk'])

        #determine light conditions based on timestamps
        if timestamp < dawn or timestamp > dusk:
            df.loc[index, 'dark'] = 1
            df.loc[index, 'part_dark'] = 0
            df.loc[index, 'light'] = 0
        elif dawn <= timestamp <= sunrise or sunset <= timestamp <= dusk:
            df.loc[index, 'dark'] = 0
            df.loc[index, 'part_dark'] = 1
            df.loc[index, 'light'] = 0
        else:
            df.loc[index, 'dark'] = 0
            df.loc[index, 'part_dark'] = 0
            df.loc[index, 'light'] = 1
      return df

def replace_rows_based_on_condition(df):
    # Ensure the DataFrame is sorted by time (if not already)
    df.sort_values('time', inplace=True)

    # Make a copy to avoid changing the original DataFrame outside the function
    new_df = df.copy()

    # Iterate through the DataFrame to apply the conditions
    for idx in range(1, len(df)):
        # Check if current row should inherit data from a previous row
        if df.iloc[idx]['none_cond']:
            # Find the last row where none_cond was False
            for j in range(idx - 1, -1, -1):
                if not df.iloc[j]['none_cond']:
                    # Copy data from the last valid row (where none_cond is False)
                    # Exclude 'time' from the columns to be copied
                    new_df.iloc[idx, df.columns != 'time'] = df.iloc[j, df.columns != 'time']
                    break

    return new_df

def replace_rows_based_on_temp(df):
    # Ensure the DataFrame is sorted by time (if not already)
    df.sort_values('time', inplace=True)

    # Make a copy to avoid changing the original DataFrame outside the function
    new_df = df.copy()

    # Initialize variables to keep track of the last valid values
    last_valid_temp = None
    last_valid_windchill = None
    last_valid_max_temp = None
    last_valid_min_temp = None

    # Iterate through the DataFrame to apply the conditions
    for idx, row in df.iterrows():
        # Check and update 'temp' column
        if row['temp'] <= 0:
            if last_valid_temp is not None:
                new_df.at[idx, 'temp'] = last_valid_temp
        else:
            last_valid_temp = row['temp']

        # Check and update 'wind_chill' column
        if row['wind_chill'] <= 0:
            if last_valid_windchill is not None:
                new_df.at[idx, 'wind_chill'] = last_valid_windchill
        else:
            last_valid_windchill = row['wind_chill']

        # Check and update 'max_temp' column
        if row['max_temp'] <= 0:
            if last_valid_max_temp is not None:
                new_df.at[idx, 'max_temp'] = last_valid_max_temp
        else:
            last_valid_max_temp = row['max_temp']

        # Check and update 'min_temp' column
        if row['min_temp'] <= 0:
            if last_valid_min_temp is not None:
                new_df.at[idx, 'min_temp'] = last_valid_min_temp
        else:
            last_valid_min_temp = row['min_temp']

    return new_df
