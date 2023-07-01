import os
import json

from src.util.fileloader import read_elements

if __name__ == "__main__":    
    versions: dict = read_elements('versions')
    extractions: dict = read_elements('extractions')

    result: dict = {
        'versions': versions,
        'extractions': extractions
    }

    with open('./merged/rqfo-data.json' , 'w') as fp:
        json.dump(result, fp)