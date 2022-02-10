import os, json
from datetime import datetime

def parse_extraction(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data

def check_extraction_validity(extraction, contributors):
    containsErrors = False

    # every extraction needs to contain a referenced extractor
    if 'extractor' not in extraction.keys() or not extraction['extractor']:
        containsErrors = True
    else:
        # make sure the responsible contributor is listed
        if extraction['extractor'] not in contributors:
            containsErrors = True
    
    # every extraction needs to contain a timestamp
    if 'timestamp' not in extraction.keys() or not extraction['timestamp']:
        containseErrors = True
    else:
        # attempt to parse the timestamp
        tmpstring = extraction['timestamp']
        try:
            datetime.strptime(tmpstring, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            containsErrors = True

    return containsErrors

# perform necessary preprocessing steps on a valid extraction object
def preprocess_extraction(extraction):
    # convert the timestamp string to an actual datetime object
    extraction['timestamp'] = datetime.strptime(extraction['timestamp'], '%Y-%m-%d %H:%M:%S')

    return extraction

# parse all available extractions
def parse_extractions(path, eligible, contributors):
    extractions = []
    for filename in eligible:
        filepath = os.path.join(path, filename+'.json')
        try:
            extraction = parse_extraction(filepath)
            containsErrors = check_extraction_validity(extraction, contributors)
            if not containsErrors:
                # preprocess the extraction object
                preprocessed = preprocess_extraction(extraction)
                extractions.append(preprocessed)
            else:
                print('The parsed extraction ' + str(filepath) + ' contained errors and was not included')
        except FileNotFoundError:
            print('The requested file ' + str(filename) + ' cannot be found on path ' + str(path)) 
    return extractions

def get_extractions(basepath: str, eligible, contributors):
    unordered = parse_extractions(basepath, eligible, contributors)
    ordered = sorted(unordered, key=lambda e: e['timestamp'], reverse=True)
    return ordered

def get_extraction(basepath: str, name, contributors):
    extractions = parse_extractions(basepath, [name], contributors)
    if len(extractions) == 1:
        return extractions[0]
    return None