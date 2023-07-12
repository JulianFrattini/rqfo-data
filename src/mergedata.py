import os
import json

from src.util.fileloader import read_elements

def convert_dict_to_list(dictionary: dict, key_name: str = 'id') -> list:
    """This method converts a dictionary, where each key-value pair represents one item of a list, back into an actual list.

    parameters:
        dictionary -- dict object with key-value pairs representing items of a list, where each value is a dictionary itself
        key_name -- name of the attribute under which the dict-key shall be added to the dict-value

    returns: a list of dict-values, where the previous key is added as an attribute
    """
    result: list = []

    for key in dictionary:
        item = dictionary[key]
        if key_name:
            item[key_name] = key
        result.append(item)

    return result

if __name__ == "__main__":    
    versions: dict = read_elements('versions')
    extractions: dict = read_elements('extractions')

    for versionid in versions:
        versions[versionid]['extraction'] = versions[versionid]['extraction']['current']

    result: dict = {
        'versions': convert_dict_to_list(versions),
        'extractions': convert_dict_to_list(extractions)
    }

    with open('./merged/rqfo-data.json' , 'w') as fp:
        json.dump(result, fp)