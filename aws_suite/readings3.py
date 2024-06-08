import csv
import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import StringIO
import pytz
from datetime import datetime
import requests

s3 = boto3.client('s3')
bucket_name = 'xxxxxxx'

def read_csv_dynamic_columns(file_path, dest, delimiter=',', fill_value='none'):
    obj = s3.get_object(Bucket=bucket_name, Key=file_path)
    lines = obj['Body'].read().decode('utf-8').splitlines()
    reader = csv.reader(lines, delimiter=delimiter)

    utc_time = obj['LastModified']
    est_zone = pytz.timezone('America/New_York')
    est_time = utc_time.astimezone(est_zone).replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

    result_rows = []
    for row in reader:
        terminal_id = row[0]
        row_data = row[1:]
        columns = dest.get(terminal_id, [])

        if columns:
            row_data = row_data[:len(columns)] + [fill_value] * (len(columns) - len(row_data))
            result_rows.append([est_time] + row_data)

    return result_rows

def threaded_automate(keys, dest):
    all_data = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_data = {executor.submit(read_csv_dynamic_columns, key, dest): key for key in keys}
        for future in as_completed(future_to_data):
            try:
                data = future.result()
                all_data.extend(data)
            except Exception as e:
                print(f"Failed to process {future_to_data[future]}: {str(e)}")
    return all_data

def upload_df_to_s3(data, bucket, key):
    output = StringIO()
    writer = csv.writer(output)
    for row in data:
        writer.writerow(row)
    output.seek(0)
    s3.put_object(Bucket=bucket, Key=key, Body=output.getvalue())
    print(f'Successfully uploaded to {bucket}/{key}')

def process_and_upload(bucket_name, dest):
    iteration = 1
    response = s3.list_objects_v2(Bucket=bucket_name)
    cont_tok = response['NextContinuationToken']
    response = s3.list_objects_v2(Bucket=bucket_name, ContinuationToken=cont_tok)
    
    while True:
        keys = [item['Key'] for item in response.get('Contents', [])]
        data = threaded_automate(keys, dest)
        new_k = f"citibikes3_it_{iteration}_data_clean.csv"
        upload_df_to_s3(data, 'cleanedcitibike', new_k)

        if not response.get('IsTruncated'):
            break
        else:
            cont_tok = response['NextContinuationToken']
            response = s3.list_objects_v2(Bucket=bucket_name, ContinuationToken=cont_tok)
            iteration += 1

def data_cleanse(rows, est_time):
    ui_dot_map_dict = {'dot-green': 1, 'dot-yellow': 2, 'dot-grey': 3, 'dot-red': 4, 'dot-pin-valet': 5}
    ui_pin_map_dict = {'pin-dock-green-most': 1, 'pin-dock-green-half': 2, 'pin-dock-yellow': 3, 'pin-dock-red': 4, 'pin-dock-grey': 5, 'pin-dock-green-all': 6, 'pin-valet': 7}
    action_dict = {'give': 1, 'take': 2, 'neutral': 3}

    cleansed_data = []
    for row in rows:
        
        row.insert(0, est_time)
        terminal = row[1]
        if len(terminal) == 6 and '.' in terminal and len(terminal.split('.')[1]) == 1:
            row[1] = terminal + "0"
    
        if len(row[1]) == 7 and '.' in row[1] and len(row[1].split('.')[1]) == 2:
            
            try:
                row[2] = int(row[2])  #capacity
                row[3] = int(row[3])  #bikes_available
                row[4] = int(row[4])  #docks_available
                row[5] = int(row[5])  #bikes_disabled
                row[6] = 1 if row[6].lower() == 'true' else 0  #renting
                row[7] = 1 if row[7].lower() == 'true' else 0  #returning
                row[8] = 1 if row[8].lower() == 'true' else 0  #ebike_surcharge_waiver
                row[9] = 1 if row[9].lower() == 'true' else 0  #installed
                row[10] = ui_dot_map_dict.get(row[10], 0)  #icon_dot_dock_layer
                row[11] = ui_dot_map_dict.get(row[11], 0)  #icon_dot_bike_layer
                row[12] = ui_pin_map_dict.get(row[12], 0)  #icon_pin_dock_layer
                row[13] = ui_pin_map_dict.get(row[13], 0)  #icon_pin_bike_layer
                row[14] = int(row[14]) if row[14].isdigit() else 0  #bike_angels_points
                row[15] = int(row[15]) if row[15].isdigit() else 0  #bike_angels_digits
                row[16] = int(row[16]) if row[16].isdigit() else -1  #ebikes_available
                row[17] = 1 if row[17] == 'available' else 0  #valet_status
                row[18] = action_dict.get(row[18], 0)  #bike_angels_action
                cleansed_data.append(row)
            except IndexError:
                #Handle errors or incomplete rows
                continue

    
    baddies_indices = [19, 20, 21, 22, 23, 24, 25]  
    for i in range(len(cleansed_data)):
        cleansed_data[i] = [col for idx, col in enumerate(cleansed_data[i]) if idx not in baddies_indices]

    return cleansed_data

if __name__ == "__main__":
    link_to_ping = 'https://layer.bicyclesharing.net/map/v1/nyc/stations'
    a = requests.get(link_to_ping).json()
    reference = {}
    for g in a['features']:
        reference[g['properties']['terminal']] = g['properties'].keys()
        
    dest = reference
    process_and_upload(bucket_name, dest)
