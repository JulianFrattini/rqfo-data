import os
import json
import pandas as pd

def read_structure(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data

def read_content(path):
    table = pd.read_csv(path, sep=',')
    return table

def read_elements(basepath, read):
    filenames = os.listdir(basepath)
    elements = {}
    for filename in filenames:
        elementname = filename.split('.')[0]
        element = read(basepath + '/' + filename)
        elements[elementname] = element
    return elements

def check_conformity(structure, taxonomy):
    fields = structure['fields']

    for field in fields:
        fn = field['name']
        if 'mandatory' in field.keys() and field['mandatory'] == True:
            # the current field is mandatory
            print(taxonomy[fn].isnull().values.any())

def analyze():
    structures = read_elements('structure', read_structure)
    taxonomies = read_elements('content', read_content)

    for taxonomy in taxonomies.keys():
        if taxonomy not in structures.keys():
            print("Error: there is no structure file found for the taxonomy '" + str(taxonomy) + "'")
        else:
            check_conformity(structures[taxonomy], taxonomies[taxonomy])

if __name__ == "__main__":
    analyze()