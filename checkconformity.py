import json
import os

def readfile(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data

def readelements(basepath, whitelist=None):
    filenames = os.listdir(basepath)
    elements = {}
    for filename in filenames:
        elementname = filename.split('.')[0]

        if whitelist == None:
            element = readfile(basepath + '/' + filename)
            elements[elementname] = element
        else:
            if elementname in whitelist:
                element = readfile(basepath + '/' + filename)
                elements[elementname] = element
    return elements

def checkobject(type, structure, object, collection) -> list[str]:
    errormsgs: list[str] = []

    for attribute in structure['attributes']:
        name = attribute['name']
        oid = object['id']

        # ATTRIBUTE: MANDATORY
        if 'mandatory' in attribute.keys() and attribute['mandatory'] == True:
            # the current field is mandatory
            if name not in object.keys() or object[name] == None:
                # check if the characteristics have a default
                if attribute['type'] in ['dimension', 'dimension cluster']:
                    if len(list(filter(lambda c: 'default' in c.keys(), attribute['characteristics']))) == 0:
                        # no default value found
                        errormsgs.append(f'Error: {type} {oid}, has no value in attribute {name}')
                else:
                    errormsgs.append(f'Error: {type} {oid}, has no value in attribute {name}')

        # ATTRIBUTE: UNIQUE
        if 'unique' in attribute.keys() and attribute['unique'] == True: 
            # obtain the values of all objects
            #values = list(map(lambda o: o[name], collection[type]))
            values = [obj[name] for obj in collection[type]]
            values.sort()
            # check that the value is unique
            if values.count(object[name]) > 1:
                errormsgs.append(f'Error: the {name} of {type} {oid} ({object[name]}) is not unique (last value: {values[-1]})')

        # ATTRIBUTE: TYPE
        if attribute['type'] == 'dimension':
            availablecharacteristics = list(map(lambda c: c['value'], attribute['characteristics']))
            # boolean attributes
            if isinstance(availablecharacteristics[0], bool):
                if object[name] not in availablecharacteristics:
                    errormsgs.append(f'Error: {type} {oid}, attribute {name} has an invalid value {object[name]} (allowed {availablecharacteristics})')
            # string dimensions
            elif isinstance(availablecharacteristics[0], str):
                if not object[name]:
                    errormsgs.append(f'Error: {type} {oid} has no value in the attribute {name}')
                else:
                    normal = object[name].lower()
                    singular = normal[:-1] if normal[-1] == 's' else normal
                    if not ((normal in availablecharacteristics) or (singular in availablecharacteristics)):
                        errormsgs.append(f'Error: {type} {oid}, attribute {name} has an invalid value {object[name]} (allowed {availablecharacteristics})')
        if attribute['type'] == 'dimension cluster':
            dimensions = list(map(lambda c: c['value'], attribute['dimensions']))
            availablecharacteristics = list(map(lambda c: c['value'], attribute['characteristics']))
            for dimension in dimensions:
                if dimension in object.keys():
                    if object[dimension] not in availablecharacteristics:
                        errormsgs.append(f'Error: {type} {oid}, dimension {dimension} has an invalid value {object[dimension]} (allowed: {availablecharacteristics})')

        elif attribute['type'] in ['ref', 'reflist']:
            references = object[name] # reference values
            target = attribute['elements'] # name of the element that is referred to

            availablerefs = [obj['id'] for obj in collection[target]]

            if attribute['type'] == 'ref':
                references = [references]

            for reference in references:
                if reference not in availablerefs:
                    errormsgs.append(f"Error: {type} {oid}'s {name} references {target} {reference}, but that element does not exist")
    return errormsgs

def compileall(extractions):
    collection = {}
    print('Compiling all objects')
    for taxonomy in taxmap:
        collection[taxonomy] = []
        for exid in extractions:
            extraction = extractions[exid]
            collection[taxonomy] = collection[taxonomy] + extraction[taxmap[taxonomy]]


        n_objects = len(collection[taxonomy]) # count number of objects in the respective taxonomy
        has_accessibility = ('accessibility' in collection[taxonomy][0]) # is the accesibility of the object relevant
        n_objects_open_access = 0
        if has_accessibility:
            open_access_objects = [obj for obj in collection[taxonomy] if obj['accessibility'].lower().startswith('open access')]
            n_objects_open_access = len(open_access_objects)
            #print([{obj['reference']} for obj in open_access_objects])

        print(f' - {n_objects} {taxmap[taxonomy]} {"" if not has_accessibility else "(" + str(n_objects_open_access) + " open access)"}')
    return collection


taxmap = {
    'factor': 'factors',
    'description': 'descriptions',
    'dataset': 'datasets',
    'approach': 'approaches'
}

if __name__ == "__main__":
    # iterate through all versions
    versions = readelements('versions')

    for version in versions:
        currentversion = versions[version]
        vc = currentversion['version']
        print(f'===========v{vc["ontology"]}.{vc["taxonomy"]}.{vc["content"]}===========')
        versionerrormsgs = []

        # obtain the structure files of the current version
        structures = readelements('structure/o' + str(currentversion['version']['ontology']) + '/t' + str(currentversion['version']['taxonomy']))

        # get all extraction files
        extractionmap = currentversion['extraction']['current']
        extractionids = list(extractionmap.values())
        extractions = readelements('extractions', whitelist=extractionids)

        # compile all objects
        collection = compileall(extractions)
        
        for exid in extractions:
            extraction = extractions[exid]
            errormsgs = []
            for structure in structures:
                # print(str(len(extraction[taxmap[structure]])) + ' ' + str(taxmap[structure]))
                for extractedobject in extraction[taxmap[structure]]:
                    errormsgs += checkobject(structure, structures[structure], extractedobject, collection)
                    versionerrormsgs = versionerrormsgs + errormsgs

            if len(errormsgs) > 0:
                print(f'-----------{exid}-----------')
                for msg in errormsgs:
                    print(f' * {msg}')

        n_remaining_errors = len(versionerrormsgs)
        if n_remaining_errors > 0:
            print('---------------------------')
            print(f'{n_remaining_errors} error{"" if n_remaining_errors == 0 else "s"} remaining')
            print('---------------------------')