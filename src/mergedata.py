import os
import json

from src.util.fileloader import read_elements

if __name__ == "__main__":
    result: dict = {}
    
    versions: dict = read_elements('versions')

    for versionfilename in versions:
        version = versions[versionfilename]
        versioninfo: dict = version['version']
        versionstring: str = f'v{versioninfo["ontology"]}.{versioninfo["taxonomy"]}.{versioninfo["content"]}'

        structures = read_elements('structure/o' + str(versioninfo['ontology']) + '/t' + str(versioninfo['taxonomy']))

        result[versionstring] = {
            'description': version['description'],
            'timestamp': version['timestamp']
        }


    print(result)