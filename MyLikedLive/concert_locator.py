# Will define functionality to parse websites for concert information
# Isaac Fisher 10.11.2022

import requests
import os
import json

class ConcertLocator:
    # Checks location for current on every instance, stored in external .txt file
    # for user continuity
    with open("loc.txt", 'r') as l:
        location = l.read()
    tm_api_key = os.getenv("TICKETMASTER_API_KEY")

    # Gets the artist key for the artist to use in __get_relevant_concerts()
    def __get_artist_key(self):
        artist_search_url = ("https://app.ticketmaster.com/discovery/v2/attractions.json?"
        "keyword={artist}&"
        "apikey={tmapi}").format(artist=self.artist, tmapi=self.tm_api_key)
        data = requests.get(artist_search_url).json()
        self.artist_key = data["_embedded"]["attractions"][0]["id"]

#TODO: Error handling on request
#TODO: Filter out irrelevant (far) concerts
#TODO: Find best practice for returning and working with results
#TODO: call __get_artist_key() and use results to filter by artist
    # Searches concerts for artist in the user's location
    def __get_relevant_concerts(self):
        self.__get_artist_key()
        concert_search_url = ("https://app.ticketmaster.com/discovery/v2/events.json?"
        "classificationName=music&" # Narrows to concerts
        "dmaId=324&" # Location
        "attractionId={artist_key}&" # Location
        "apikey={tmapi}").format(artist_key=self.artist_key, tmapi=self.tm_api_key) # authorizes
        data = requests.get(concert_search_url).json()
        print(data["_embedded"]["events"][0])

#TODO: Ping server for artist's name and get their dmaID
#TODO: Currently searches by location, url construction needs to be changed
    # Basic constructor, creates URL for later use in webscraping
    def __init__(self, artist):
        self.artist = artist
        self.relevant_concerts = self.__get_relevant_concerts()

cl1 =  ConcertLocator("Men I Trust")
