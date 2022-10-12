# Will define functionality to parse websites for concert information
# Isaac Fisher 10.11.2022

import requests
import os

class ConcertLocator:
    # Checks location for current on every instance, stored in external .txt file
    # for user continuity
    with open("loc.txt", 'r') as l:
        location = l.read()

#TODO: Figure out why ticketmaster api is returning a 401 error code
#TODO: Filter out irrelevant (far) concerts
#TODO: Find best practice for returning and working with results
    def __getRelevantConcerts(self):
        data = requests.get(self.url)
        print(data)

    # Basic constructor, creates URL for later use in webscraping
    def __init__(self, artist):
        self.artist = artist
        self.url = ("https://app.ticketmaster.com/discovery/v2/events.json?"
        "classificationName=music&" # Narrows to concerts
        "dmaId=324&" # Artist
        "apikey={{{tmapi}}}").format(tmapi=os.getenv("TICKETMASTER_API_KEY")) # authorizes
        print(os.getenv("TICKETMASTER_API_KEY"))
        self.__getRelevantConcerts()

cl1 =  ConcertLocator("Men I Trust")
