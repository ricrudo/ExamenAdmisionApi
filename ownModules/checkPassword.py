import json
import os
import datetime

def currentTime():
    current = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
    return current.strftime('%Y-%m-%dT%H:%M:%S')

def checkPassword(password, instrumento, profile):
    if profile == 'monitor':
        filename = os.sep.join(['data', 'monitors.dlt'])
    elif profile == 'jury':
        filename = os.sep.join(['data', 'juries.dlt'])
    with open(filename, 'r') as f:
        data = json.load(f)
    response = False
    if profile == 'monitor' and data[instrumento]['cedula'] == password:
        response = data[instrumento]['nombre']
    elif profile == 'jury':
        for person, cedula in data[instrumento].items():
            if cedula == password:
                response = {'cedula':cedula, 'nombre': person}
                break
    createPersonLog(password)
    return response

def createPersonLog(cedula):
    filename = os.sep.join(['data', 'personalLog'])
    if not os.path.exists(filename):
        os.mkdir(filename)
    filename = os.sep.join(['data', 'personalLog', 'monitors.dlt'])
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('{}')


