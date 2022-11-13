# A set of useful methods for working with resources/settings.json

import json
import os.path

# Writes a value to the given setting in resources/settings.json
def write_to_config(setting, value):
    config_path = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(config_path, "..", "..", "resources", "config.json")

    with open(config_path, "r+") as config_raw:
        config = json.load(config_raw)
        config[setting] = value
        config_raw.seek(0)
        config_raw.truncate()
        json.dump(config, config_raw, indent=4)

# Specifically fetches the location code from resources/settings.json
def get_location_code():
    config_path = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(config_path, "..", "..", "resources", "config.json")

    with open(config_path, "r") as config_raw:
        config = json.load(config_raw)
        return config["locationCode"]
