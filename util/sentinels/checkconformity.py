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

# return a list of indices identifying a set of entries
def get_id_list(df, fn):
    if fn == 'ID':
        # if the currently investigated field is the ID, then use the dataframe index, as the ID might be NaN
        return list(df.index.values)
    else:
        # if the currently investigated field is not the ID, try to use the dedicated ID for identification (as long as no ID is NaN)
        if len(df[df['ID'].isnull()]) > 0:
            return list(df.index.values)
        else:
            return list(df['ID'])

def check_conformity(structure, taxonomy):
    fields = structure['fields']

    for field in fields:
        fn = field['name']
        if 'mandatory' in field.keys() and field['mandatory'] == True:
            # the current field is mandatory
            missingvalues = taxonomy[taxonomy[fn].isnull()]
            if len(missingvalues) > 0:
                print('Error: mandatory field ' + str(fn) + ' is empty for the following entries with the following index: ' + str(get_id_list(missingvalues, fn)))

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