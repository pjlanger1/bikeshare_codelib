import pandas as pd
import requests
import zipfile
from io import BytesIO

def get_triphistory(yearmonth):
    url = f'https://s3.amazonaws.com/tripdata/{yearmonth}-citibike-tripdata.csv.zip'
    response = requests.get(url)

    #Check if the request was successful (status code 200)
    if response.status_code == 200:

        zip_file = zipfile.ZipFile(BytesIO(response.content))

        for file_name in zip_file.namelist():
            if file_name.endswith('.csv'):
                csv_file = zip_file.open(file_name)
                df = pd.read_csv(csv_file)
                return df
    else:
        print("400: No File")

        # Perform any operations with the DataFrames

