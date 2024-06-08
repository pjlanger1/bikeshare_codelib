import requests
import pandas as pd
import time
import json
import os

def get_directory_contents(owner, repo, directory_sha, token):
    """
    Fetch the contents of a directory using its SHA.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{directory_sha}?recursive=1"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['tree']  #this will be a list of items in the directory
    else:
        print("Failed to fetch directory contents:", response.status_code)
        return None

def fetch_file_content(url):
   """
    returns from blob url the json file, invokes update_rate_limit_from_response
    """
    global rate_limit_remaining
    response = requests.get(url, headers=headers)
    update_rate_limit_from_response(response)
    
    if response.status_code == 200:
        return response.json()  #parse JSON content directly
    else:
        print(f"Failed to fetch file: {response.status_code}")
        return None

def update_rate_limit_from_response(response):
  """
    manages sleep if rate limit is hit
    """
    global rate_limit_remaining
    rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', rate_limit_remaining))
    if rate_limit_remaining <= 10:  #simple check to avoid hitting the limit
        reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600))  #default to one hour
        pause_duration = reset_time - time.time() + 10  #adding a 10-second buffer
        print(f"Pausing for {pause_duration} seconds due to rate limit...")
        time.sleep(pause_duration)
        rate_limit_remaining = 5000  #assume reset to a safe default

rate_limit_remaining = 5000  #initialize with a default value or fetch from GitHub API

#function to update rate limit and handle the sleep logic
def update_rate_limit_from_response(response, data_frames, dump_counter):
    global rate_limit_remaining
    rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', rate_limit_remaining))
    
    if rate_limit_remaining <= 10:  #simple check to avoid hitting the limit
        print(f"Rate limit is low. Dumping current data and pausing...")
        dump_data(data_frames, dump_counter)  #dump the data before sleeping
        
        reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600))  #default to one hour later
        pause_duration = reset_time - time.time() + 10  #adding a 10-second buffer
        print(f"Pausing for {pause_duration} seconds due to rate limit...")
        time.sleep(pause_duration)
        
        rate_limit_remaining = 5000  #assume reset to a safe default

#function to dump data to a CSV file
def dump_data(data_frames, counter):
    if data_frames:
        full_data = pd.concat(data_frames, ignore_index=True)
        dump_path = f'partial_data_{counter}.csv'
        counter += 1
        full_data.to_csv(dump_path, index=False)
        print(f"Data dumped to {dump_path}.")

#main loop to process files
def process_files(contents):
    data_frames = []
    visited_paths = set()
    dump_counter = 1

    for file_info in contents:
        if file_info['path'] not in visited_paths:
            visited_paths.add(file_info['path'])
            file_content = fetch_file_content(file_info['url'], data_frames, dump_counter)
            if file_content is not None:
                df = pd.DataFrame([file_content])
                data_frames.append(df)

    #final dump after processing all files
    if data_frames:
        dump_data(data_frames, dump_counter)
        

  
