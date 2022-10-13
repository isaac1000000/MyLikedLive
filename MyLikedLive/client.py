# The main file of the project, used to fetch data and report to user
# Created by Isaac Fisher 10.11.2022

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from concert_locator import ConcertLocator
import os.path

# This scope allows for reading of recently listened
scope = "user-read-recently-played"
redirect_uri = "http://localhost:8888"
client_id = "dc6bf3fc568940c5afb5607c4281fb7e"

# Creates a spotipy instance with the determined scope
# Spotify object grabs SPOTIPY_CLIENT_SECRET from environment
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
    redirect_uri=redirect_uri, scope=scope))

# Creates a set of the unique artists in the user's recently played
query_results = sp.current_user_recently_played()
unique_artists = set()
for item in query_results['items']:
    for artist in item['track']['artists']:
        unique_artists.add(artist['name'])

# Print all recent unique artists
print("Lately, you've been listening to: ")
print(", ".join(unique_artists))

#TODO: Error handling for incorrect location code
# Gets user's location from resources/loc.txt, stored externally for continuity
filepath = os.path.abspath(os.path.dirname(__file__))
filepath = os.path.join(filepath, "../resources/loc.txt")
with open(filepath, 'r') as l:
    location = l.read().strip()

print("Searching for local concerts from these artists...\n")
# Iterates through artists to check for applicable concerts then prints
for artist in unique_artists:
    concerts = ConcertLocator(artist, location)
    if concerts.exists():
        print(concerts)


#TODO: Make a nicer-looking interface, or at least more responsive
#TODO: Figure out how to do user-end logins instead of whatever is going on here
#TODO: Define custom exceptions & outline error protocol for concert_locator,
    # including maybe finding a better way to avoid ratelimit errors
