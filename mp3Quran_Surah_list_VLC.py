import csv
import json
import requests
"""
This Python script performs the following actions:

Prompts the user for input on which Surahs (chapters) of the Quran to include in a playlist.
Generates a playlist name based on the user's input and prints it to the console.
Processes the user's input to create a list of Surah numbers. If the input includes a range (e.g. "1:5"), a list of numbers is created from the range. If the input includes a list of numbers separated by commas (e.g. "1,2,3"), a list is created from the input.
Sends a GET request to the mp3quran API to retrieve a list of reciters and their corresponding audio files.
Loads the JSON data from the API response and gets the list of reciters.
Opens a CSV file for writing and creates a CSV writer object. The script then writes the column names and iterates through the list of reciters, writing each row to the CSV file. The script also writes the information for each moshaf (edition of the Quran) for each reciter.
Splits the list of Surahs for each moshaf into a list of individual Surah numbers and appends the URL of the audio file for each Surah to a list of URLs.
Opens a text file for writing and writes each URL in the list of URLs to the file.
Iterates through the list of Surah numbers specified by the user and appends the URL of the audio file for each Surah to a separate list of URLs.
Opens a new file with the playlist name specified by the user and writes an XSPF playlist XML document to the file using the list of URLs for the Surahs specified by the user.
"""
# Prompt the user for input on which Surahs to include in the playlist
Surah_nums_inp = input('Enter the numbers of Surah separated by : OR , :-\n')

# Generate a playlist name based on the user's input
playlist_name = ('quranList_' + Surah_nums_inp + '.xspf').replace(':', 'to')
print(playlist_name)

# Process the user's input to create a list of Surah numbers
if ':' in Surah_nums_inp:
    # If the input includes a range (e.g. "1:5"), create a list of numbers from the range
    Surah_nums = range(int(Surah_nums_inp.replace(' ', '').split(':')[0]), int(Surah_nums_inp.replace(' ', '').split(':')[1])+1)
elif ',' in Surah_nums_inp:
    # If the input includes a list of numbers separated by commas (e.g. "1,2,3"), create a list from the input
    Surah_nums = Surah_nums_inp.replace(' ', '').split(',')

print(Surah_nums)

# URL of the mp3quran API
url = 'https://www.mp3quran.net/api/v3/reciters?language=ar'

# List to store the URLs of all audio files
mp3QuranURL = []

# List to store the URLs of the audio files for the Surahs specified by the user
listen_URL = []

# Send a GET request to the API to retrieve a list of reciters and their corresponding audio files
response = requests.get(url)

# Load the JSON data from the response
data = response.json()

# Get the list of reciters from the JSON data
reciters = data['reciters']

# Open a CSV file for writing
with open('reciters.csv', 'w', newline='', encoding="utf-8") as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)

    # Write the column names
    writer.writerow(['id', 'name', 'letter','moshaf_id','moshaf_name','moshaf_server','moshaf_surah_total','moshaf_surah_list'])

    # Iterate through the list of reciters and write each row to the CSV file
    for reciter in reciters:
        for moshaf in reciter['moshaf']:
            # Write the reciter's information and the information for each moshaf (edition of the Quran)
            writer.writerow([reciter['id'],reciter['name'],reciter['letter'],moshaf['id'],moshaf['name'],moshaf['server'],moshaf['surah_total'],moshaf['surah_list']])
            
            # Split the list of Surahs for the moshaf into a list of individual Surah numbers
            surah_list = moshaf['surah_list'].split(',')
            for surah in surah_list:
                mp3QuranURL.append(moshaf['server'] + f'{int(surah):03d}' +'.mp3')
print("Finished writing CSV file")

with open('reciters.txt', 'w',encoding="utf-8") as mp3QuranURLs:
    for URL in mp3QuranURL:
        mp3QuranURLs.write(URL+'\n')
        
        for Surah_num in Surah_nums:
            if f'{int(Surah_num):03d}' in URL :
                listen_URL.append(URL)            
print("Finished writing TXT file")



#Opens a new file with the playlist name specified by the user and writes an XSPF playlist XML document to the file using the list of URLs for the Surahs specified by the user.

with open(playlist_name, 'w',encoding="utf-8") as quranList:
    quranList.write("""<?xml version="1.0" encoding="UTF-8"?>
    <playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
            <title>Playlist</title>
            <trackList>""")
    i = 0
    for link in listen_URL:
        quranList.write("""		<track>
                            <location>"""+link+"""</location>
                            <extension application="http://www.videolan.org/vlc/playlist/0">
                                    <vlc:id>"""+str(i)+"""</vlc:id>
                                    <vlc:option>network-caching=1000</vlc:option>
                            </extension>
                    </track>""")
        i+=1

    quranList.write("""	</trackList>
            <extension application="http://www.videolan.org/vlc/playlist/0">
                    <vlc:node title="qurango.xspf">""")
    for i in range(len(listen_URL)):
        quranList.write('			<vlc:item tid="'+str(i)+'"/>')

    quranList.write("""		</vlc:node>
            </extension>
    </playlist>
    """)
print("Finished writing VLC file")
