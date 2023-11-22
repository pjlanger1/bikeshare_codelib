#Transit Ventures' Knowledge Graph is based off of the CECL Centerline publication's most recent distribution,
## but for the computer vision modules, we're instead going to work off of the bike route data native to
## the NYC DOT's GraphQL databases, which serve the webcam application.

#fetchdata() method sends one get request and one post request to two separate layers of the DOT's API.
## to acquire raw, realtime data for the purposes of extracting the subset of bike-lane adjacent cameras

#compare() method builds a bounding box for each segment (note: some segments do not represent straight lines,
## in these cases, we iterate through points computing a max polygon), returning a dictionary of camera ids with
## coordinates inside of the bounding box. Will add functionality to further refine test for presence on or near line segment.

##Example Usage:
## one, two = fetchdata()
## dictionary_o = compare(one,two)


import pandas as pd
import requests
import json

def fetchdata():
  #retrieving the cameras list
    df = pd.DataFrame(requests.get('https://webcams.nyctmc.org/api/cameras/').json())
  #retrieving the bike lane geometry from GraphQL store
    url = 'https://webcams.nyctmc.org/bikes/graphql'

    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'Origin': 'https://webcams.nyctmc.org',
    'Accept-Language': 'en-US,en;q=0.9',
    'Host': 'webcams.nyctmc.org',
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://webcams.nyctmc.org/map',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',}

    data = {
    'query': '''query { layers { links { points { latitude longitude}}}}''','variables': {}}

    dic = requests.post(url, json=data, headers=headers).json()['data']['layers'][0]['links']

    return df, dic


def compare(df, dic):
    newdict = {}
    for index, row in df.iterrows():
        for i in dic:
            min_x = float('inf')
            min_y = float('inf')
            max_x = float('-inf')
            max_y = float('-inf')
            #Calculate the bounding box
            for j in i['points']:
                min_x = min(min_x, j['latitude'])
                max_x = max(max_x, j['latitude'])
                min_y = min(min_y, j['longitude'])
                max_y = max(max_y, j['longitude'])
            #Check if the point is within the bounding box
            if min_x <= row['latitude'] <= max_x and min_y <= row['longitude'] <= max_y:
                newdict[row['id']] = True
                break  
            else:
                newdict[row['id']] = False
    return newdict
