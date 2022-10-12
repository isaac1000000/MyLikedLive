# Will define functionality to parse websites for concert information
# Isaac Fisher 10.11.2022

import requests
import os
import json

class ConcertLocator:
    # Checks location for current on every instance, stored in external .txt file
    # for user continuity
    with open("loc.txt", 'r') as l:
        location = l.read().strip()
    tm_api_key = os.getenv("TICKETMASTER_API_KEY")

#TODO: Error handling on request
    # Gets the artist key for the artist to use in __get_relevant_concerts()
    def __get_artist_key(self):
        artist_search_url = ("https://app.ticketmaster.com/discovery/v2/attractions.json?"
        "keyword={artist}&"
        "apikey={tmapi}").format(artist=self.artist, tmapi=self.tm_api_key)
        data = requests.get(artist_search_url).json()
        if data["page"]["totalElements"]:
            self.artist_key = data["_embedded"]["attractions"][0]["id"]
            return self.artist_key
        self.artist_key = 0
        return 0

#TODO: Error handling on request
    # Searches concerts for artist in the user's location
    def __get_relevant_concerts(self):
        self.__get_artist_key()
        concert_search_url = ("https://app.ticketmaster.com/discovery/v2/events.json?"
        "dmaId={location}&" # Location
        "attractionId={artist_key}&" # Location
        "apikey={tmapi}").format(location=self.location, artist_key=self.artist_key, tmapi=self.tm_api_key) # authorizes
        data = requests.get(concert_search_url).json()
        relevant_concerts = list()
        # Checks for empty return from the request
        if data["page"]["totalElements"]:
            for event in data["_embedded"]["events"]:
                relevant_concerts.append({"name":event["name"],
                    "date":event["dates"]["start"]["localDate"],
                    "venue":event["_embedded"]["venues"][0]["name"]})
        return relevant_concerts

    # Basic constructor, creates URL for later use in webscraping
    def __init__(self, artist):
        self.artist = artist
        self.relevant_concerts = self.__get_relevant_concerts()
