from cProfile import label
import os
import json
from numpy import NaN
import pandas as pd
import re

def read_structure(path, structure=None):
    with open(path, 'r') as f:
        data = json.load(f)
        return data

def read_content(path, structure):
    # define specific converters
    converters = {}
    # go through the structure and find all fields, that are reflists
    for field in structure['fields']:
        if field['type'] in ['reflist', 'menum']:
            converters[field['name']] = (lambda x: (x.split(';') if len(x)>0 else None))

    table = pd.read_csv(path, sep=',', converters=converters, na_values=[' ', ''])
    return table

def read_elements(basepath, read, structures=None):
    filenames = os.listdir(basepath)
    elements = {}
    for filename in filenames:
        elementname = filename.split('.')[0]
        element = read(basepath + '/' + filename, (structures[elementname] if structures != None else None))
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

def check_conformity(structures, taxonomies, taxkey):
    structure = structures[taxkey]
    taxonomy = taxonomies[taxkey]
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
            # for enums, make sure that the used value is contained in the list of possible values
            values = field['values']
            nonconformant = taxonomy[~taxonomy[fn].isin(values)]
            if len(nonconformant) > 0:
                print('Error: field ' + str(fn) + ' only takes values ' + str(values) + ', but the objects of the following ID contain other values: ' + str(nonconformant['ID'].values))
        elif field['type'] == 'menum':
            # for multiple enums, make sure that all used values are contained in the list of possible values
            values = field['values']
            nonconformant = taxonomy.apply(lambda row: not all(value in values for value in row[fn]), axis=1)
            nonconformantindices = list(nonconformant[nonconformant].index.values)
            if len(nonconformantindices) > 0:
                print('Error: the following objects contain values in the multiple-enumerator ' + str(fn) + ' which are not in the list of allowed values: ' + str(nonconformantindices))
        elif field['type'] == 'reflist':
            # for reflists, make sure that all referenced keys are contained in the referenced taxonomy objects

            # obtain the targeted reference keys
            targetname = field['elements']
            targetkeys = set(taxonomies[targetname]['ID'].values)

            # obtain the source reference keys
            sourcekeys = set()
            taxonomy.apply(lambda row: (sourcekeys.update(row[fn]) if row[fn] else None), axis=1)
            if len(sourcekeys) > 0:
                # check if there are keys in the source set that are not contained in the target set
                invalidkeys = list(sourcekeys-targetkeys)
                if len(invalidkeys) > 0:
                    print('Error: in the ' + str(taxkey) + ' taxonomy, the following keys referring to objects of the ' + str(targetname) + ' taxonomy are not valid: ' + str(invalidkeys))


def analyze():
    structures = read_elements('structure', read_structure)
    taxonomies = read_elements('content', read_content, structures)

    for taxkey in taxonomies.keys():
        if taxkey not in structures.keys():
            print("Error: there is no structure file found for the taxonomy '" + str(taxkey) + "'")
        else:
            check_conformity(structures, taxonomies, taxkey)

if __name__ == "__main__":
    analyze()