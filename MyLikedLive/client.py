# The main file of the project, used to fetch data and report to user
# Created by Isaac Fisher 10.11.2022

import spotipy
from spotipy.oauth2 import SpotifyPKCE
from concert_locator import ConcertLocator
import os.path
import json

# This scope allows for reading of recently listened
scope = "user-read-recently-played"

# Gets necessary values for spotify and
settings_filepath = os.path.abspath(os.path.dirname(__file__))
settings_filepath = os.path.join(settings_filepath, "..", "resources", "config.json")
with open(settings_filepath, 'r') as s:
    settings = json.load(s)
    location = settings["locationCode"]
    client_id = settings["spotifyClientID"]
    redirect_uri = settings["spotifyRedirectURI"]
    ConcertLocator.tm_api_key = settings["ticketmasterAPIKey"]


# Creates a spotipy instance with the determined scope
# SpotifyPKCE handles all auth flow without needing a client secret
sp = spotipy.Spotify(auth_manager=SpotifyPKCE(client_id=client_id,
    redirect_uri=redirect_uri, scope=scope))

# Creates a set of the unique artists in the user's recently played
query_results = sp.current_user_recently_played()
unique_artists = set()
for item in query_results['items']:
    for artist in item['track']['artists']:
        unique_artists.add(artist['name'])

# Print all recent unique artists
print()
print("Lately, you've been listening to: ")
print(", ".join(unique_artists))
print()

print("Searching for local concerts from these artists...\n")
progress = 0
all_concerts = []
# Iterates through artists to check for applicable concerts then prints
for artist in unique_artists:
    concerts = ConcertLocator(artist, location)
    if concerts.exists():
        all_concerts.append(concerts)
    progress += 1/len(unique_artists)
    print("{:-<30}".format("\r|" + "█"*int(progress*30)) + "|", end="")

print("\n")
for concert in all_concerts:
    print(concert)
print()


#TODO: Define custom exceptions & outline error protocol for concert_locator,
    # including maybe finding a better way to avoid ratelimit errors
#TODO: GUI
