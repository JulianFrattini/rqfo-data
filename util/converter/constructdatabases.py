import os, json
from datetime import datetime

def parse_extraction(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data

def check_extraction_validity(extraction):
    containsErrors = False

    # every extraction needs to contain a referenced extractor
    if 'extractor' not in extraction.keys() or not extraction['extractor']:
        containseErrors = True
    
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
def parse_extractions(path):
    filenames = os.listdir(path)

    extractions = []
    for filename in filenames:
        filepath = os.path.join(path, filename)
        extraction = parse_extraction(filepath)
        containsErrors = check_extraction_validity(extraction)
        if not containsErrors:
            # preprocess the extraction object
            preprocessed = preprocess_extraction(extraction)
            extractions.append(preprocessed)
    
    return extractions

# group all extraction objects by its reference and order it by timestamp
def order_extractions(extractions):
    exts = {}

    references = set(extraction['reference'] for extraction in extractions)
    for reference in references:
        eligible_extractions = list(filter(lambda extraction: extraction['reference'] == reference, extractions))
        ordered = sorted(eligible_extractions, key=lambda d: d['timestamp'], reverse=True)
        exts[reference] = ordered

    return exts

if __name__ == "__main__":
    extractions = parse_extractions('extractions')
    order_extractions(extractions)
    #print(extractions)