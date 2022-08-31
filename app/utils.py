import json
from os import path


def writeJson(filename, data):

    def write(listObj):
        with open(filename, 'w') as json_file:
                json.dump(listObj, json_file, 
                                    indent=4,  
                                    separators=(',',': '))

    try:
        listObj = []

        # Check if file exists
        # else create file
        if path.isfile(filename) is False:
            # create file with empty list
            write(listObj)
        
        # Read JSON file
        with open(filename) as fp:
            listObj = json.load(fp)
        
        listObj.append(data)
        
        # add rules to existing json file
        write(listObj)

        
        return True
    except Exception as error:
        print(error)
    return False