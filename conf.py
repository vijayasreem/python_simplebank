import json
import os.path
import threading
from etc import Debug

lock = threading.Lock()

def Write(filename, config) -> bool:
    """Returns True when the file operation was successful, otherwise False."""
    try:
        with open(filename, "w") as f:
            json.dump(config, f, indent=4)
            Debug(f"Wrote configuration to {filename}.")
            retVal = True
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
        for _ in range(4):
            if lock.acquire(blocking=False):
                try:
                    with open(filename, "r") as f:
                        config = json.load(f)
                        Debug(f"Successfully read configuration file: {filename}.")
                        retVal = config
                except Exception as x:
                    print(f"An error occurred during reading {filename}: {x}")
                    retVal = None
                finally:
                    lock.release()
                break
        else:
            raise Exception("Unable to acquire lock after retries")
    return retVal

# Unit tests for multi-threaded file access scenarios
def test_multi_threaded_access():
    filename = "config.json"
    default = {"key": "value"}

    def read_config():
        config = Read(filename, default)
        assert config == {"key": "value"}

    threads = []
    for _ in range(10):
        t = threading.Thread(target=read_config)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

test_multi_threaded_access()