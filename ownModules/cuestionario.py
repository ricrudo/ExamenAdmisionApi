import os
import json

def set_cuestionario(data):
    if not os.path.exists('institutions'):
        os.mkdir('institutions')
    filename = os.sep.join(['institutions', data['institution'] + '.dlt'])
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    blankData = {}
    blankData['institution'] = 'Blank'
    for section in data:
        if isinstance(data[section], dict):
            blankData[section] = {}
            for category in data[section]:
                blankData[section][category] = 0
    blankData['time'] = 0
    filename = os.sep.join(['institutions', 'Blank.dlt'])
    with open(filename, 'w') as f:
        json.dump(blankData, f, indent=4)


def get_cuestionario(institution):
    filename = os.sep.join(['institutions', institution + '.dlt'])
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return 'NotFound'
