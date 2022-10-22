# Authenticates spotify, gathers recent artists, and finds relevant concerts
# Created by Isaac Fisher 10.11.2022

import spotipy
from spotipy.oauth2 import SpotifyPKCE
from concert_locator import ConcertLocator
import os.path
import json
from utils import exceptions

class SpotifyScraper:
    # Scope necessary for all calls in this class
    scope = "user-read-recently-played"

    # Gets necessary values from resources/config.json and ensures validity
    def gather_settings(self):
        try:
            settings_filepath = os.path.abspath(os.path.dirname(__file__))
            settings_filepath = os.path.join(settings_filepath, "..", "resources", "config.json")
            with open(settings_filepath, 'r') as s:
                settings = json.load(s)
                self.location = settings["locationCode"]
                assert self.location and isinstance(self.location, int), ["locationCode", "not_an_integer"]
                self.client_id = settings["spotifyClientID"]
                assert self.client_id and isinstance(self.client_id, str), ["spotifyClientID", "not_a_string"]
                self.redirect_uri = settings["spotifyRedirectURI"]
                assert self.redirect_uri and isinstance(self.redirect_uri, str), ["spotifyRedirectURI", "not_a_string"]
                ConcertLocator.tm_api_key = settings["ticketmasterAPIKey"]
                assert ConcertLocator.tm_api_key and ConcertLocator.tm_api_key, ["ticketMasterAPIKey", "not_a_string"]
        except FileNotFoundError:
            raise exceptions.ConfigFaultException()
        except KeyError as err:
            raise exceptions.ConfigFaultException("'" + err.args[0] + "'", type="not_found")
        except AssertionError as err:
            raise exceptions.ConfigFaultException("'" + err.args[0][0] + "'", type=err.args[0][1])

    # Creates a spotipy instance with the necessary scope
    # SpotifyPKCE handles all auth flow without needing a client secret
    def create_spotify_instance(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyPKCE(client_id=self.client_id,
            redirect_uri=self.redirect_uri, scope=self.scope))
        try:
            assert self.sp.current_user() # Makes sure authentication was successful
        except:
            raise exceptions.FailedToAuthorizeException(endpoint="SpotifyPKCE web auth")

    # Get recently played from user's spotify
    def gather_recently_played(self):
        try:
            query_results = self.sp.current_user_recently_played()
            self.unique_artists = set()
            for item in query_results['items']:
                for artist in item['track']['artists']:
                    self.unique_artists.add(artist['name'])
        except:
            raise exceptions.RequestFaultException("Spotify API request endpoint")

    # Gets artists' local concerts from ticketmaster
    def find_artist_concerts(self):
        progress = 0
        self.all_concerts = []
        # Iterates through artists to check for applicable concerts then prints
        for artist in self.unique_artists:
            concerts = ConcertLocator(artist, self.location)
            if concerts.exists():
                self.all_concerts.append(concerts)
            if self.loading_bar:
                progress += 1/len(self.unique_artists)
                print("{:-<30}".format("\r|" + "█"*int(progress*30)) + "|", end="")

    def __init__(self, loading_bar=False):
        self.loading_bar = loading_bar
        self.gather_settings()
        self.create_spotify_instance()
        self.gather_recently_played()
