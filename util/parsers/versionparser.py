import os, json
from datetime import datetime

timestampkey = "timestamp"

# read one single json file
def read_structure(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data

# perform necessary preprocessing steps on a valid extraction object
def update_timestamp(extraction, strformat):
    # convert the timestamp string to an actual datetime object
    extraction[timestampkey] = datetime.strptime(extraction[timestampkey], strformat)

    return extraction

# parse all existing structure files in the given basepath
def parse_versions(basepath):
    filenames = os.listdir(basepath)
    elements = []
    for filename in filenames:
        elementname = filename.split('.')[0]
        element = read_structure(basepath + '/' + filename)
        element = update_timestamp(element, '%Y-%m-%d %H:%M:%S')
        elements.append(element)
    return elements

def get_latest_version(basepath):
    # obtain all recorded versions
    all_versions = parse_versions(basepath)

    # order the versions by the timestamp field
    ordered = sorted(all_versions, key=lambda v: v[timestampkey], reverse=True)

    return ordered[0]