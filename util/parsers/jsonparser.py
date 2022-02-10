import json

# read one single json file
def jsonparse(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data