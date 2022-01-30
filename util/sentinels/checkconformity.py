import os
import json
import pandas as pd
import re

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

        # ATTRIBUTE: MANDATORY
        if 'mandatory' in field.keys() and field['mandatory'] == True:
            # the current field is mandatory
            missingvalues = taxonomy[taxonomy[fn].isnull()]
            if len(missingvalues) > 0:
                print('Error: mandatory field ' + str(fn) + ' is empty for the following entries with the following index: ' + str(get_id_list(missingvalues, fn)))

        # ATTRIBUTE: UNIQUE
        if 'unique' in field.keys() and field['unique'] == True:
            # the values of the current field should be unique
            duplicates = taxonomy.duplicated(subset=fn, keep='first')
            indices = list(duplicates[duplicates].index.values)
            if len(indices) > 0:
                print('Error: unique field ' + str(fn) + ' has duplicate values at the following indices: ' + str(indices))

        # ATTRIBUTE: TYPE
        if field['type'] == 'identifier':
            form = str(field['format'])
            pattern = re.compile(form)
            matches = taxonomy[fn].apply(lambda v: pattern.match(v) == None)
            nonconformant = list(matches[matches].index.values)
            if len(nonconformant) > 0:
                noncindices = taxonomy.iloc[nonconformant]
                print('Error: field ' + str(fn) + ' needs to follow the pattern ' + str(form) + ', but the objects with the following IDs are non-compliant: ' + str(list(noncindices['ID'].values)))
        elif field['type'] == 'enum':
            values = field['values']
            nonconformant = taxonomy[~taxonomy[fn].isin(values)]
            if len(nonconformant) > 0:
                print('Error: field ' + str(fn) + ' only takes values ' + str(values) + ', but the objects of the following ID contain other values: ' + str(nonconformant['ID'].values))
                print(nonconformant)

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