# The main file of the project, used to fetch data and report to user
# Created by Isaac Fisher 10.11.2022

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-recently-played"
redirect_uri = "https://google.com"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_recently_played()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " - ", track['name'])
