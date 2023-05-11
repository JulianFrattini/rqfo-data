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
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data
    except OSError:
        return None
    
def read_elements(basepath: str, whitelist: list[str]=None) -> dict:
    """Reads all JSON files in a base path and creates a map from the file names to the JSON file converted to a dictionary.

    parameters:
        basepath -- Path of the directory containing the files of interest
        whitelist -- Optional list of file names (without file extensions); If provided, read only those files

    returns:
        elements -- Dictionary mapping file names to the parsed JSON files in dictionary format.
    """
    filenames_in_path: list[str] = os.listdir(basepath)
    #print(filenames_in_path)

    elements = {}
    for filename in filenames_in_path:
        # retrieve the name of the file (filename minus the file extension)
        elementname = filename.split('.')[0]

        if whitelist == None or elementname in whitelist:
            element = read_file(basepath + '/' + filename)
            elements[elementname] = element
            
    return elements