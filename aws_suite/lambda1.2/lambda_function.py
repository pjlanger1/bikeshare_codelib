import boto3
import json
from datetime import datetime
from zoneinfo import ZoneInfo  #python 3.9+ for timezone handling
import requests

def lambda_handler(event, context):
    
    #the url
    link_to_ping = 'https://gbfs.lyft.com/gbfs/1.1/bkn/en/station_status.json'
    
    #default values for each key
    kwd = {
        'legacy_id': 'na', 
        'last_reported': '999', 
        'num_bikes_available': -1, 
        'num_bikes_disabled': -1, 
        'num_ebikes_available': -1, 
        'num_docks_available': -1, 
        'num_docks_disabled': -1, 
        'num_scooters_available': -1, 
        'num_scooters_unavailable': -1, 
        'is_renting': -1, 
        'is_returning': 0, 
        'is_installed': 0
    }
    
    #fetch the data
    a = requests.get(link_to_ping).json()
    
    #process the JSON data and build CSV content
    dest = {}
    for g in a['data']['stations']:
        dest[g['station_id']] = [g.get(key, default) for key, default in kwd.items()]
    
    csv_string = ""
    for key, values in dest.items():
        csv_string += f"{key},{','.join(map(str, values))}\n"

    #set timezone to New York (America/New_York)
    ny_tz = ZoneInfo("America/New_York")
    update_time = datetime.now(ny_tz)

    #construct folder structure (year/month/day) and the filename with hour and minute
    folder_structure = f"{update_time.year}/{update_time.month:02}/{update_time.day:02}/"
    filename = f"{update_time.hour:02}_{update_time.minute:02}.csv"
    s3_key = folder_structure + filename


    bucket_name = 'jsonpublicfeed2'  
    
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, s3_key).put(Body=csv_string)

    return {
        'statusCode': 200,
        'body': ''}
