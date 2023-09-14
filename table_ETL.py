##Utility Function for time-rounding.
#Used For Resampling irregularly spaced time series

import datetime
import math
date_format = '%Y-%m-%dT%H:%M:%S%z'

def round_time(dtimestr):
    current_datetime = datetime.datetime.strptime(dtimestr, date_format)
    minutes = current_datetime.minute
    seconds = current_datetime.second
    minutes_to_round = math.ceil(minutes / 15) * 15
    if minutes_to_round == 60:
        current_datetime += datetime.timedelta(hours=1)
        rounded_datetime = current_datetime.replace(minute=0, second=0)
    else:
        rounded_datetime = current_datetime.replace(minute=minutes_to_round, second=0)
    return rounded_datetime

##Utility Function for creating the date scaffold before loading to table
def date_scaffold_create(result):
#Convert the string to a datetime object

    date_format = '%Y-%m-%dT%H:%M:%S%z'
    start_date = result.iloc[0,0]
    end_date = result.iloc[-1,0]
    date_list = []

    current_date = start_date
    while current_date <= end_date:
        if current_date.hour >= 5 and current_date.hour <= 23:
            date_list.append(current_date)
        current_date += datetime.timedelta(minutes=15)
        
    return date_list

#The Pepe Function takes a filepath as an argument, returns NoneType
#It orchestrates the pre-ETL table load work involved in building the postgreSQL data.

import csv
import os
import time
import pandas as pd

def pepe(filename):
    filename_final = os.path.basename(filename)
    start_time1 = time.time()
    data = []

#Open the CSV file
    with open(filename, 'r') as file:
        # Create a CSV reader
        csv_reader = csv.DictReader(file)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append each row as a dictionary to the data list
            data.append(row)

#formatting data:
    for b in data:
        b['date'] = round_time(b['date'])
        if b['bikes_disabled'] == '':
            b['bikes_disabled'] = 0
        if b['docks_disabled'] == '':
            b['docks_disabled'] = 0

    #DataFrame Manipulation
    df = pd.DataFrame(data)
    df['docks_disabled'] = df['docks_disabled'].astype(float)
    df['bikes_disabled'] = df['bikes_disabled'].astype(float)
    df['bike_angels_points'] = df['bike_angels_points'].astype(float)
    df['bikes_available'] = df['bikes_available'].astype(float)
    df['docks_available'] = df['docks_available'].astype(float)
    #df['dt_str'] = df['date'].astype(str)
    result = df.groupby('date').mean().round(0)
    result = result.reset_index()

    #call function
    date_list = date_scaffold_create(result)

    #making mapping tables
    mapping_dict_docks_d = dict(zip(result['date'], result['docks_disabled']))
    mapping_dict_bikes_d = dict(zip(result['date'], result['bikes_disabled']))
    mapping_dict_angels = dict(zip(result['date'], result['bike_angels_points']))
    mapping_dict_docks_a = dict(zip(result['date'], result['docks_available']))
    mapping_dict_bikes_a = dict(zip(result['date'], result['bikes_available']))

    date_list_df = pd.DataFrame(date_list,columns = {'date'})

    date_list_df['docks_disabled'] = date_list_df['date'].map(mapping_dict_docks_d)
    date_list_df['bikes_disabled'] = date_list_df['date'].map(mapping_dict_bikes_d)
    date_list_df['angels_points'] = date_list_df['date'].map(mapping_dict_angels)
    date_list_df['docks_available'] = date_list_df['date'].map(mapping_dict_docks_a)
    date_list_df['bikes_available'] = date_list_df['date'].map(mapping_dict_bikes_a)

    #copying
    df_filled = date_list_df.copy()

    #rolling mean fill to compensate for regular outages in the scraping methodology
    rolling_mean = df_filled.rolling(window=14,min_periods=1).mean().round(0) #handling intermittent problems
    df_filled = df_filled.fillna(rolling_mean)

    #linear interpolation for more persistent errors
    df_filled['docks_available'] = df_filled['docks_available'].interpolate(method='linear').round(0)
    df_filled['bikes_available'] = df_filled['bikes_available'].interpolate(method='index').round(0)
    df_filled['docks_disabled'] = df_filled['docks_disabled'].interpolate(method='linear').round(0)
    df_filled['bikes_disabled'] = df_filled['bikes_disabled'].interpolate(method='linear').round(0)
    df_filled['angels_points'] = df_filled['angels_points'].interpolate(method='linear').round(0)
    
    output_directory='' #fill this in
    output_file = os.path.join(output_directory, filename_final)
    with open(output_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(df_filled.values.tolist())
    
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(elapsed_time1)
    
    
