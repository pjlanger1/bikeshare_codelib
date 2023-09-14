#Imports
import csv
import os
from typing import Dict, List

#This utility method takes a directory path as an argument and creates a dictionary that runs the later consolidate_csv module.
def dict_f_create(dir_structure) -> Dict[str, List[int]:
  dirs_list = [dir_structure]
for i in range(2,9):
    dirs_list.append(dir_structure + '_' + str(i)) #in this case we had 9 directories to parse.
  
dict_files = {}
for i in range(0,len(dirs_list)):
    for file in os.listdir(dirs_list[i]):
        start_index = file.find("df_data_station_") + len("df_data_station_")
        end_index = file.find(".csv")
        substring = file[start_index:end_index]
        if substring in dict_files.keys():
            dict_files[substring].append(i)
        else:
            # If the key doesn't exist, create a new key with a list containing the value
            dict_files[substring] = [i]
        
return dict_files


#Method for consolidating multiple CSV files in a dictionary
def consolidate_csv(dict_files):
  for g in dict_files.keys():
      consolidated_data = []
      output_directory = ".../website_scrape_2022to082323"
      stri = "df_data_station_" + g + ".csv"
      if os.path.exists(stri):
              continue
      #create new file in directory here?
      for f in dict_files[g]:
          header_written = False
          sn = dirs_list[f]+"/"+stri
          with open(sn, 'r') as file:
              csv_reader = csv.reader(file)
              
              # Skip the header row if needed
              header = next(csv_reader, None)
              
              # Append the data rows to the consolidated list
              for row in csv_reader:
                  consolidated_data.append(row)
                  
      output_file = os.path.join(output_directory, stri)
      with open(output_file, 'w', newline='') as file:
          csv_writer = csv.writer(file)
          
          # Write the header row only for the first file
          if not header_written and header:
              csv_writer.writerow(header)
              header_written = True
          
          # Write the data rows
          csv_writer.writerows(consolidated_data)
