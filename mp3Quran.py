url = 'https://mp3quran.net/api/v3/reciters'


import requests
import json
import csv


 
r = requests.get(url)





data = r.json()
 
# Opening JSON file and loading the data
# into the variable data
with open('reciters.json') as json_file:
    data = json.load(json_file)
 
employee_data = data['reciters']
 
# now we will open a file for writing
data_file = open('data_file.csv', 'w',encoding="utf-8")
 
# create the csv writer object
csv_writer = csv.writer(data_file)
 
# Counter variable used for writing
# headers to the CSV file
count = 0
 
for emp in employee_data:
    if count == 0:
 
        # Writing headers of CSV file
        header = emp.keys()
        csv_writer.writerow(header)
        count += 1
 
    # Writing data of CSV file
    csv_writer.writerow(emp.values())
 
data_file.close()
