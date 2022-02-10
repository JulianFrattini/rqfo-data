import json

from util.parsers.jsonparser import jsonparse
from util.parsers.structureparser import parse
from util.parsers.versionparser import get_latest_version
from util.parsers.extractionparser import get_extraction

def compile():
    # parse all structure files and contributors
    structures = parse('structure')
    contributors = jsonparse('contributors.json')

    # parse the latest version
    version = get_latest_version('versions')

    # from the latest version: parse all included extraction files & identify all extractions, that are new
    eligible_extractions = {}
    for reference in list(version['extraction']['current'].keys()):
        eligible_extractions[reference] = get_extraction('extractions', version['extraction']['current'][reference], list(map(lambda c: c['ID'], contributors)))
    print(eligible_extractions['R024'])

    # for each new extraction: verify that it matches the format defined in the structure file

    # for each new extraction: make sure it 

    return None

if __name__ == "__main__":
    compile()