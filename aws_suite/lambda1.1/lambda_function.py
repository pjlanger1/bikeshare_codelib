import boto3
import json
from datetime import datetime
import requests

def lambda_handler(event, context):
    #GBFS bike feed 'link_to_ping'
    kwd = {'legacy_id':'na','last_reported':'999','num_bikes_available':-1,'num_bikes_disabled':-1,'num_ebikes_available':-1,'num_docks_available':-1,'num_docks_disabled':-1,'num_scooters_available':-1,'num_scooters_unavailable':-1,'is_renting':-1,'is_returning':0,'is_installed':0}
    a = requests.get(link_to_ping).json()
    dest = {}
    for g in a['data']['stations']:
        dest[g['station_id']] = [g.get(key, default) for key, default in kwd.items()]
    
    csv_string = ""
    for key, values in dest.items():
        csv_string += f"{key},{','.join(map(str, values))}\n"
    
    update_time = datetime.now()
    update_time_1 = f"{update_time.year}_{update_time.month}_{update_time.day}_{update_time.hour}_{update_time.minute}.csv"

    bucket_name = 'jsonpublicfeed'

    s3_key = update_time_1

    #upload the CSV string as a file to S3
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, s3_key).put(Body=csv_string)
        
        
    return {
        'statusCode': 200,
        'body': ''
    }
