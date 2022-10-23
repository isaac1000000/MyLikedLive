import csv
import os.path

def get_locations():
    locations = []

    dma_id_filepath = os.path.abspath(os.path.dirname(__file__))
    dma_id_filepath = os.path.join(dma_id_filepath, "..", "..", "resources", "dmaIDs.csv")

    with open(dma_id_filepath) as dma_ids_raw:
        dma_ids = csv.reader(dma_ids_raw)
        for row in dma_ids:
            if row[0] == "DMA ID":
                break
        for row in dma_ids:
            locations.append(row[1])
    return locations

def get_ids():
    ids = dict()

    dma_id_filepath = os.path.abspath(os.path.dirname(__file__))
    dma_id_filepath = os.path.join(dma_id_filepath, "..", "..", "resources", "dmaIDs.csv")

    with open(dma_id_filepath) as dma_ids_raw:
        dma_ids = csv.reader(dma_ids_raw)
        for row in dma_ids:
            if row[0] == "DMA ID":
                break
        for row in dma_ids:
            ids[row[1]] = int(row[0])
    return ids
