#Transit Ventures' Knowledge Graph is based off of the CECL Centerline publication 

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
