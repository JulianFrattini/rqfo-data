import os, json

# read one single json file
def read_structure(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data

# parse all existing structure files in the given basepath
def parse(basepath):
    filenames = os.listdir(basepath)
    elements = {}
    for filename in filenames:
        elementname = filename.split('.')[0]
        element = read_structure(basepath + '/' + filename)
        elements[elementname] = element
    return elements