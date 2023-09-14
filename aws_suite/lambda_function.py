import requests
import boto3
import json
#import csv
#import pandas as pd
from datetime import datetime


def lambda_handler(event, context):
    # Web scraping
    link_to_ping = 'https://layer.bicyclesharing.net/map/v1/nyc/stations'
    a = requests.get(link_to_ping).json()
    dest = {}
    for g in a['features']:
        dest[g['properties']['terminal']] = g['properties']
        
    
    csv_string = ""
    for terminal, properties in dest.items():
        csv_string += f"{terminal},{','.join([str(value) for value in properties.values()])}\n"
    #print(csv_string[0:120])
    update_time = datetime.now()
    update_time_1 = f"{update_time.year}_{update_time.month}_{update_time.day}_{update_time.hour}_{update_time.minute}.csv"

    bucket_name = 'jsonprivfeed'  # Replace with your S3 bucket name
    #b_name = "100001/20180223/" + bucket_name
    s3_key = update_time_1  # Replace with the desired S3 key for the file

    #Upload the CSV string as a file to S3
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, s3_key).put(Body=csv_string)
    

    return {
           'statusCode': 200,
           'body': 'test'
    }
