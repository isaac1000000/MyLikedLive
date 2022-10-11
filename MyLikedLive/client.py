# The main file of the project, used to fetch data and report to user
# Created by Isaac Fisher 10.11.2022

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# This scope allows for reading of recently listened
scope = "user-read-recently-played"
redirect_uri = "https://google.com"

# Creates a spotipy instance with the determined scope
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Creates a set of the unique artists in the user's recently played
query_results = sp.current_user_recently_played()
unique_artists = set()
for item in query_results['items']:
    for artist in item['track']['artists']:
        unique_artists.add(artist['name'])

print(unique_artists)
