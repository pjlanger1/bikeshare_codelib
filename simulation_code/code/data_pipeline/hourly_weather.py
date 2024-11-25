import pandas as pd
def reaggregate_hourly(df):
    agg_funcs = {'max_temp': 'mean', 'min_temp': 'mean','temp': 'mean','wind_chill': 'mean','heat_index': 'mean','wind_speed': 'mean','wind_direction': 'mean','wind_gust': 'mean','visibility': 'mean','cloud_cover': 'mean','humid': 'mean','precip': 'sum','snow': 'sum','snow_depth': 'max','clear_cond': 'max','none_cond': 'max','overcast_cond': 'max','partially_cloudy_cond': 'max','rain_cond': 'max','snow_cond': 'max','dark': 'max','part_dark': 'max','light': 'max','holiday': 'max'}
    df['time'] = pd.to_datetime(df['time'])
    df['time'] = df['time'].apply(lambda x: x.replace(minute=0, second=0))
    df = df.drop(['minute_cos','day_of_week_sin','day_of_week_cos'],axis = 1)
    d2 = df.groupby('time').agg(agg_funcs)
    return d2.reset_index()
