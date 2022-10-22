from spotify_scraper import SpotifyScraper

# Print all recent unique artists
ss = SpotifyScraper(loading_bar=True)

print()
print("Lately, you've been listening to: ")
print(", ".join(ss.unique_artists))
print()

print("Searching for local concerts from these artists...\n")


print("\n")
for concert in ss.all_concerts:
    print(concert)
print()

#TODO: GUI
