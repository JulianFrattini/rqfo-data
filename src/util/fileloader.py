import os
import json

def read_file(path: str) -> dict:
    """Reads a JSON file at the given path and returns it as a dictionary.

    parameters:
        path -- URL of the JSON file

    returns:
        data -- JSON file parsed to a python dictionary
        None -- if the file does not exist      
    """
    with open(path, 'r') as f:
        data = json.load(f)
        return data