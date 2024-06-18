import pandas as pd
import requests
import zipfile
from io import BytesIO
from scipy.spatial import cKDTree
#This serves as an API endpoint wrapper for data stored on Citibike/Lyft's Public AWS Bucket, serving ride history.

def get_triphistory(yearmonth):
    if yearmonth <= 201612: #formatting check
        url = f'https://s3.amazonaws.com/tripdata/{yearmonth}-citibike-tripdata.zip'
    else:
        url = f'https://s3.amazonaws.com/tripdata/{yearmonth}-citibike-tripdata.csv.zip'
        
    response = requests.get(url)

    dtype_mapping = {
    'start_station_id': str,
    'end_station_id': str}

    #Check if the request was successful (status code 200)
    if response.status_code == 200:

        zip_file = zipfile.ZipFile(BytesIO(response.content))

        for file_name in zip_file.namelist():
            if file_name.endswith('.csv'):
                csv_file = zip_file.open(file_name)
                df = pd.read_csv(csv_file,dtype=dtype_mapping)
                return df
    else:
        print("400: No File")

def create_adjacency_list(df):

    #preprocessing raw downloaded tripfile:
    df_stations = df[['start_station_id','start_lat','start_lng']]
    df_stations_aug = df[['end_station_id','end_lat','end_lng']]
    df_stations_aug.columns = ['start_station_id','start_lat','start_lng']
    concatenated_df = pd.concat([df_stations, df_stations_aug], ignore_index=True)
  
    unique_df = concatenated_df.drop_duplicates(subset=['start_station_id'])
  
    #Extract station_id, lat, and lon from DataFrame
    station_data = unique_df[['start_station_id', 'start_lat', 'start_lng']]
    
    #Set 'start_station_id' as the index
    station_data.set_index('start_station_id', inplace=True)

    #Create a KD-tree for efficient nearest neighbor search
    kdtree = cKDTree(station_data[['start_lat', 'start_lng']].values)

    adjacency_list = {}

    for station_id, (lat, lon) in station_data.iterrows():
        #Query the KD-tree for the four closest neighbors
        _, indexes = kdtree.query((lat, lon), k=5)
        
        #Exclude the current point itself from the neighbors
        neighbors = list(station_data.iloc[indexes].index)
        
        #Check if the station_id is in the neighbors list before removing
        if station_id in neighbors:
            neighbors.remove(station_id)
        
        neighbors = neighbors[:4]

        #Store neighbors in the adjacency list
        adjacency_list[station_id] = neighbors

    return adjacency_list



