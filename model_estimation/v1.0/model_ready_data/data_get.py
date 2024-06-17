import pandas as pd
import requests
import zipfile
from io import BytesIO
import os

def get_triphistory(yearmonth):
    if yearmonth <= 201612 or yearmonth in [202404,202405]:
        url = f'https://s3.amazonaws.com/tripdata/{yearmonth}-citibike-tripdata.zip'
    else:
        url = f'https://s3.amazonaws.com/tripdata/{yearmonth}-citibike-tripdata.csv.zip'
        
    response = requests.get(url)
    dtype_mapping = {'start_station_id': str, 'end_station_id': str}

    if response.status_code == 200:
        zip_file = zipfile.ZipFile(BytesIO(response.content))
        fnames = zip_file.namelist()
        df_list = []
        for file_name in fnames:
            if file_name.endswith('.csv'):
                try:
                    with zip_file.open(file_name) as csv_file:
                        df = pd.read_csv(csv_file, dtype=dtype_mapping, encoding='utf-8')
                        df_list.append(df)
                except UnicodeDecodeError:
                    with zip_file.open(file_name) as csv_file:
                        df = pd.read_csv(csv_file, dtype=dtype_mapping, encoding='iso-8859-1')
                        df_list.append(df)
        if df_list:
            return pd.concat(df_list, ignore_index=True)
        else:
            print("No CSV files found in the ZIP.")
    else:
        print("Failed to fetch data:", response.status_code)

def consolidate_data_agg(df):
    # Convert to datetime and round to the nearest 15 minutes
    df['started_at'] = pd.to_datetime(df['started_at']).dt.round('15min')
    df['ended_at'] = pd.to_datetime(df['ended_at']).dt.round('15min')
    
    df['start_station_id'] = df['start_station_id'].astype(str)
    df['end_station_id'] = df['end_station_id'].astype(str)
    
    df['start_station_id'] = df['start_station_id'].apply(lambda x: f"{x}0" if len(x) == 6 and '.' in x and len(x.split('.')[1]) == 1 else x)
    df['end_station_id'] = df['end_station_id'].apply(lambda x: f"{x}0" if len(x) == 6 and '.' in x and len(x.split('.')[1]) == 1 else x)

    df = df[df['start_station_id'].str.match(r'^\d{4}\.\d{2}$')]
    df = df[df['end_station_id'].str.match(r'^\d{4}\.\d{2}$')]
    
    # Group by start and end stations, times, and rideable types, then count rides
    start_counts = df.groupby(['start_station_id', 'started_at', 'rideable_type'])['ride_id'].count().reset_index(name='start_count')
    end_counts = df.groupby(['end_station_id', 'ended_at', 'rideable_type'])['ride_id'].count().reset_index(name='end_count')
    
    # Create a DataFrame with unique station IDs and rideable types from both start and end station IDs
    unique_stations = pd.concat([
        start_counts[['start_station_id', 'rideable_type']].rename(columns={'start_station_id': 'station_id'}),
        end_counts[['end_station_id', 'rideable_type']].rename(columns={'end_station_id': 'station_id'})
    ]).drop_duplicates().reset_index(drop=True)
    
    # Rename columns for consistent merging
    start_counts.rename(columns={'start_station_id': 'station_id', 'started_at': 'time'}, inplace=True)
    end_counts.rename(columns={'end_station_id': 'station_id', 'ended_at': 'time'}, inplace=True)
    
    # Perform left joins to align start and end counts for each station and rideable type
    station_counts = unique_stations.merge(start_counts, on=['station_id', 'rideable_type'], how='left') \
                                    .merge(end_counts, on=['station_id', 'time', 'rideable_type'], how='left').fillna(0)
    
    # Ensure counts are integers
    station_counts['start_count'] = station_counts['start_count'].astype(int)
    station_counts['end_count'] = station_counts['end_count'].astype(int)
    
    return station_counts

def senddata(df,path,name):
    fn = "citibike_" + str(name) + ".parquet"
    fname = os.path.join(path,fn)
    df.to_parquet(fname, engine='pyarrow', compression='snappy')
