#importing all the packages
import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import pandas as pd
from fp.fp import FreeProxy

#reading in the guider file
with open('xxx') as f:
    lines = str(f.read())
    
#data separated like this:
dat = [j['label'] for j in json.loads(lines)]
ind = [j['value'] for j in json.loads(lines)]
data_metric = ['docks_available','bikes_available','bike_angels_points','bikes_disabled','docks_disabled']

#cleaning up list
xx = [True] * len(dat)
for v in range(0,len(xx)):
    if isinstance(ind[v],str):
        xx[v] = False


ind_2 = [x for x in ind if not isinstance(x, str)]
dat_2 = np.array(dat)[xx]
print(len(dat_2),len(ind_2))
header = {'Content-Type': 'application/json'}

#UPDATING THE GUIDER LIST
new = json.loads(requests.get('xxxx').text)['props']['children'][0]['props']['options']
ind_new_1 = [j['label'] for j in new]
dat_new_1 = [j['value'] for j in new]
import socket
from urllib3.connection import HTTPConnection

HTTPConnection.default_socket_options = (
    HTTPConnection.default_socket_options + [
        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
        #(socket.SOL_TCP, socket.TCP_KEEPIDLE, 45),
        (socket.SOL_TCP, socket.TCP_KEEPINTVL, 10),
        (socket.SOL_TCP, socket.TCP_KEEPCNT, 6)
    ]
)

fail_list = []
for number in dat_1:
    proxy = {"https":"https://xxx.xxxx.xxxxx"}
    df = pd.DataFrame()
    max_len = 0
    for metric in data_metric:
        payload_5 = '{{"output":"citibike-graph.figure","outputs":{{"id":"citibike-graph","property":"figure"}},"inputs":[{{"id":"search-type-radio","property":"value","value":"{metric}"}},{{"id":"station-dropdown","property":"value","value":[{number}]}},{{"id":"crossfilter-xaxis-type","property":"value","value":168}}],"changedPropIds":["crossfilter-xaxis-type.value"]}}'.format(number = number, metric = metric)
        try:
            r = requests.post(url ='xxx', data=payload_5, headers = header)
        except ConnectionError:
            r = requests.post(url ='xxx', data=payload_5, headers = header)
        except ValueError:
            r = requests.post(url ='xxx', data=payload_5, headers = header)
        
        print("LOGGING: "+ metric + " for " + str(number))
        print("STATUS CODE" + str(r.status_code))
        
        g = json.loads(r.text)
        try:
            if metric == 'docks_available': #first iteration of the loop
                m_1 = pd.Series(g['response']['citibike-graph']['figure']['data'][0]['x'])
                df['date'] = m_1.values
                m_2 = pd.Series(g['response']['citibike-graph']['figure']['data'][0]['y'])
                df['docks_available'] = m_2.values
                max_len = len(df['docks_available'])
            elif metric == 'docks_disabled':
                m_3 = pd.Series(g['response']['citibike-graph']['figure']['data'][0]['y'])[0:max_len]
                df['docks_disabled'] = m_3.values
                filename = '/df' + "_data_station_" + str(number) + '.csv'
                df.to_csv(filename)
            else: 
                m_4 = pd.Series(g['response']['citibike-graph']['figure']['data'][0]['y'])[0:max_len]
                df[metric] = m_4.values
        except ValueError:
            fail_list.append(str(number))
        except IndexError:
            fail_list.append(str(number))
        
        print("data appended...")
    #updated
    
    #updated
    
