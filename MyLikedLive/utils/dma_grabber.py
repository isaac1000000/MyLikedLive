# Useful methods for working with the DMA information in resources/DMAIDs.csv
# Isaac Fisher
import csv
import os.path

# Gets all locations' names as strings
def get_locations():
    locations = []

    dma_id_filepath = os.path.abspath(os.path.dirname(__file__))
    dma_id_filepath = os.path.join(dma_id_filepath, "..", "..", "resources", "dmaIDs.csv")

    with open(dma_id_filepath, "r") as dma_ids_raw:
        dma_ids = csv.reader(dma_ids_raw)
        for row in dma_ids:
            if row[0] == "DMA ID":
                break
        for row in dma_ids:
            locations.append(row[1])
    return locations

# Returns a dictionary of all locations and their IDS
def get_ids():
    ids = dict()

    dma_id_filepath = os.path.abspath(os.path.dirname(__file__))
    dma_id_filepath = os.path.join(dma_id_filepath, "..", "..", "resources", "dmaIDs.csv")

    with open(dma_id_filepath, "r") as dma_ids_raw:
        dma_ids = csv.reader(dma_ids_raw)
        for row in dma_ids:
            if row[0] == "DMA ID":
                break
        for row in dma_ids:
            ids[row[1]] = int(row[0])
    return ids

# Gets the location with a given location code
def get_location(locationCode):
    dma_id_filepath = os.path.abspath(os.path.dirname(__file__))
    dma_id_filepath = os.path.join(dma_id_filepath, "..", "..", "resources", "dmaIDs.csv")

    with open(dma_id_filepath, "r") as dma_ids_raw:
        dma_ids = csv.reader(dma_ids_raw)
        for row in dma_ids:
            if row[0].strip() == str(locationCode):
                return row[1]
        return None
