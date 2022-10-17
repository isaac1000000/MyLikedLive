# Will define functionality to parse websites for concert information
# Isaac Fisher 10.11.2022

import requests
import json
import time

class ConcertLocator:

    tm_api_key = ""

#TODO: Error handling on request
    # Gets the artist key for the artist to use in __get_relevant_concerts()
    def __get_artist_key(self):
        artist_search_url = ("https://app.ticketmaster.com/discovery/v2/attractions.json?"
        "keyword={artist}&"
        "apikey={tmapi}").format(artist=self.artist, tmapi=self.tm_api_key)
        data = requests.get(artist_search_url).json()
        # Ensures that any one-off faults are ignored and the result was not empty
        if (not "fault" in data.keys()) and data["page"]["totalElements"]:
            self.artist_key = data["_embedded"]["attractions"][0]["id"]
            return self.artist_key
        self.artist_key = 0
        return 0

#TODO: Error handling on request
    # Searches concerts for artist in the user's location
    def __get_relevant_concerts(self):
        self.__get_artist_key()
        time.sleep(.25) # Avoids ratelimit errors
        concert_search_url = ("https://app.ticketmaster.com/discovery/v2/events.json?"
        "dmaId={location}&" # Location
        "attractionId={artist_key}&" # Artist
        "apikey={tmapi}").format(location=self.location,
        artist_key=self.artist_key, tmapi=self.tm_api_key)
        data = requests.get(concert_search_url).json()
        relevant_concerts = list()
        # Checks for empty return from the request
        if (not "fault" in data.keys()) and data["page"]["totalElements"]:
            for event in data["_embedded"]["events"]:
                relevant_concerts.append({"name":event["name"],
                    "date":event["dates"]["start"]["localDate"],
                    "venue":event["_embedded"]["venues"][0]["name"]})
        time.sleep(.25) # Avoids ratelimit errors
        return relevant_concerts

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

    # Gives toString method for debugging and output
    def __str__(self):
        if self.exists():
            result_list = []
            for concert in self.relevant_concerts:
                result_list.append("[{artist}]: {name} is playing at the venue \"{venue}\""
                " on {date}".format(artist=self.artist, name=concert["name"],
                venue=concert["venue"], date=concert["date"]))
            return "\n".join(result_list)
        else:
            return None
