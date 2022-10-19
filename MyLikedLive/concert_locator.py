# Defines functionality to parse websites for concert information
# Isaac Fisher 10.11.2022

import requests
import json
import time
from utils import exceptions

class ConcertLocator:

    # This value will be set in client.py when config.json is parsed
    tm_api_key = ""

    # Gets the artist key for the artist to use in __get_relevant_concerts()
    def __get_artist_key(self):
        # Creates search url for artist's ID number with auth included
        artist_search_url = ("https://app.ticketmaster.com/discovery/v2/attractions.json?"
        "keyword={artist}&"
        "apikey={tmapi}").format(artist=self.artist, tmapi=self.tm_api_key)
        data = requests.get(artist_search_url)
        status = data.status_code
        if status == 401: # Code for unauthorized request attempt
            raise exceptions.FailedToAuthorizeException(endpoint=artist_search_url)
        elif status == 200: # Code for successful request
            data = data.json()
            # Gets artist_key if it exists, returns dummy value otherwise
            if data["page"]["totalElements"]:
                self.artist_key = data["_embedded"]["attractions"][0]["id"]
                return self.artist_key
            self.artist_key = 0
            return 0
        elif status == 429: # Code for ratelimit issue
            time.sleep(.25)
            # Sleeps then calls method again, generally a times/second thing
            return self.__get_artist_key()
        else: # Handles all other request errors
            raise exceptions.RequestFaultException(artist_search_url, response_code=status)



    # Searches concerts for artist in the user's location
    def __get_relevant_concerts(self):
        self.__get_artist_key()
        # Creates search url for artist and location with auth included
        concert_search_url = ("https://app.ticketmaster.com/discovery/v2/events.json?"
        "dmaId={location}&" # Location
        "attractionId={artist_key}&" # Artist
        "apikey={tmapi}").format(location=self.location,
        artist_key=self.artist_key, tmapi=self.tm_api_key)
        data = requests.get(concert_search_url)
        status = data.status_code
        if status == 401: # Code for unauthorized request attempt
            raise exceptions.FailedToAuthorizeException(endpoint=concert_search_url)
        elif status == 200: # Code for successful request
            data = data.json()
            relevant_concerts = list()
            # Parse to get necessary data for relevant_concerts
            if data["page"]["totalElements"]:
                for event in data["_embedded"]["events"]:
                    relevant_concerts.append({"name":event["name"],
                        "date":event["dates"]["start"]["localDate"],
                        "venue":event["_embedded"]["venues"][0]["name"]})
            return relevant_concerts
        elif status == 429: # Code for ratelimit issue
            time.sleep(.25)
            # Sleeps then calls method again, generally a times/second thing
            return self.__get_relevant_concerts()
        else: # Handles all other request errors
            raise exceptions.RequestFaultException(concert_search_url, response_code=status)

    # Basic constructor, calls __get_relevant_concerts()
    def __init__(self, artist, location):
        self.artist = artist
        self.location = location
        self.relevant_concerts = self.__get_relevant_concerts()

    # Checks for presence of matching concerts
    def exists(self):
        if self.relevant_concerts:
            return True
        else:
            return False

    # toString method for output
    def __str__(self):
        if self.exists():
            result_list = []
            for concert in self.relevant_concerts:
                result_list.append("[{artist}]: {name} is playing at the venue \"{venue}\""
                " on {date}".format(artist=self.artist, name=concert["name"],
                venue=concert["venue"], date=concert["date"]))
            return "\n".join(result_list)
        else:
            return ""
