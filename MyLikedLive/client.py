# The main file of the project, used to fetch data and report to user
# Created by Isaac Fisher 10.11.2022

import spotipy
from spotipy.oauth2 import SpotifyPKCE
from concert_locator import ConcertLocator
import os.path
import json
from utils import exceptions

# This scope allows for reading of recently listened
scope = "user-read-recently-played"

# Gets necessary values from resources/config.json and ensures validity
try:
    settings_filepath = os.path.abspath(os.path.dirname(__file__))
    settings_filepath = os.path.join(settings_filepath, "..", "resources", "config.json")
    with open(settings_filepath, 'r') as s:
        settings = json.load(s)
        location = settings["locationCode"]
        assert location and isinstance(location, int), ["locationCode", "not_an_integer"]
        client_id = settings["spotifyClientID"]
        assert client_id and isinstance(client_id, str), ["spotifyClientID", "not_a_string"]
        redirect_uri = settings["spotifyRedirectURI"]
        assert redirect_uri and isinstance(redirect_uri, str), ["spotifyRedirectURI", "not_a_string"]
        ConcertLocator.tm_api_key = settings["ticketmasterAPIKey"]
        assert ConcertLocator.tm_api_key and isinstance(ConcertLocator.tm_api_key, str), ["ticketMasterAPIKey", "not_a_string"]
except FileNotFoundError:
    raise exceptions.ConfigFaultException()
except KeyError as err:
    raise exceptions.ConfigFaultException("'" + err.args[0] + "'", type="not_found")
except AssertionError as err:
    raise exceptions.ConfigFaultException("'" + err.args[0][0] + "'", type=err.args[0][1])

# Creates a spotipy instance with the necessary scope
# SpotifyPKCE handles all auth flow without needing a client secret
try:
    sp = spotipy.Spotify(auth_manager=SpotifyPKCE(client_id=client_id,
        redirect_uri=redirect_uri, scope=scope))
    assert sp.current_user() # Makes sure authentication was successful
except:
    raise exceptions.FailedToAuthorizeException(endpoint="SpotifyPKCE web auth")

# Creates a set of the unique artists in the user's recently played
try:
    query_results = sp.current_user_recently_played()
    unique_artists = set()
    for item in query_results['items']:
        for artist in item['track']['artists']:
            unique_artists.add(artist['name'])
except:
    raise exceptions.RequestFaultException("Spotify API request endpoint")

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

#TODO: GUI
