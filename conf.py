# sb_conf.py

import json
import os.path
from etc import Debug
# Simple JSON Handler


def Write(filename, config) -> bool:
    """Returns True when the file operation was successful, otherwise False."""
    try:
        with open(filename, "w") as f:
            json.dump(config, f, indent=4)
            Debug(f"Wrote configuration to {filename}.")
            retVal = True
            f.close()

    except Exception as e:
        print("Failed to write config file: ", e)
        retVal = False
        return retVal


def Read(filename, default) -> dict:
    """
    Returns a dictionary loaded from a JSON file located at the given path, or a default if file doesn't exist.
    Return None when an error occurs during the file operation.
    """

    if not os.path.isfile(filename):
        Debug("Config file doesn't exist. Creating...")
        Write(filename, default)
        Debug(f"Config file {filename} created.")
        retVal = default
    else:
        try:
            with open(filename, "r") as f:
                config = json.load(f)
                Debug(f"Successfully read configuration file: {filename}.")
                retVal = config
                f.close()

        except Exception as x:
            print(f"An error occurred during reading {filename}: {x}")
            retVal = None
    return retVal
