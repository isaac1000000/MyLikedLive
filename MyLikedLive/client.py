# The main file of the project, used to fetch data and report to user
# Created by Isaac Fisher 10.11.2022

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from concert_locator import ConcertLocator

# This scope allows for reading of recently listened
scope = "user-read-recently-played"
redirect_uri = "https://google.com"

# Creates a spotipy instance with the determined scope
# Spotify object grabs SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET from environment
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri=redirect_uri, scope=scope))

# Creates a set of the unique artists in the user's recently played
query_results = sp.current_user_recently_played()
unique_artists = set()
for item in query_results['items']:
    for artist in item['track']['artists']:
        unique_artists.add(artist['name'])

# Print all recent unique artists
print("Lately, you've been listening to: ")
print(", ".join(unique_artists))

# Iterates through artists to check for applicable concerts then prints
for artist in unique_artists:
    concerts = ConcertLocator(artist)
    if concerts.exists():
        print(concerts)


#TODO: use list of artists to search ticketing websites
#TODO: make a nicer-looking interface, or at least more responsive
#TODO: figure out how to do user-end logins instead of whatever is going on here
