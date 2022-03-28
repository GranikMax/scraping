#?method=artist.getinfo&artist=Cher&api_key=YOUR_API_KEY&format=json
import json

import requests
from pprint import pprint
url = 'https://ws.audioscrobbler.com/2.0/'


artist = 'Linkin Park'
api_key = 'f61b625caa0d64b0687dffa6118bc88f'
params = {'method': 'artist.getinfo',
          'artist': artist,
          'api_key': api_key,
          'format': 'json'}

response = requests.get(url, params=params)
m_data = response.json()
with open ('my.json', 'w') as file:
    json.dump(m_data, file, indent=3)
pprint(m_data)