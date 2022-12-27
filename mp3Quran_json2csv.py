import csv
import json
import requests

Surah_nums = input('Enter the numbers of Surah separated by , :\n')

# URL of the JSON data
url = 'https://www.mp3quran.net/api/v3/reciters?language=ar'
mp3QuranURL =[]
listen_URL =[]
# Send a GET request to the URL and store the response
response = requests.get(url)

# Load the JSON data from the response
data = response.json()

# Get the list of reciters from the JSON data
reciters = data['reciters']

# Open a CSV file for writing
with open('reciters.csv', 'w', newline='',encoding="utf-8") as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)

    # Write the column names
    writer.writerow(['id', 'name', 'letter','moshaf_id','moshaf_name','moshaf_server','moshaf_surah_total','moshaf_surah_list'])

    # Iterate through the list of reciters and write each row to the CSV file
    for reciter in reciters:
        for moshaf in reciter['moshaf']:
            writer.writerow([reciter['id'],reciter['name'],reciter['letter'],moshaf['id'],moshaf['name'],moshaf['server'],moshaf['surah_total'],moshaf['surah_list']])
            surah_list = moshaf['surah_list'].split(',')
            for surah in surah_list:
                mp3QuranURL.append(moshaf['server'] + f'{int(surah):03d}' +'.mp3')
print("Finished writing CSV file")

with open('reciters.txt', 'w',encoding="utf-8") as mp3QuranURLs:
    for URL in mp3QuranURL:
        mp3QuranURLs.write(URL+'\n')
        for Surah_num in Surah_nums.replace(' ','').split(','):
            listen_URL.append(URL)            
print("Finished writing TXT file")




