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
