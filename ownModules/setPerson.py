import json
import os
import ownModules

def getData(profile):
    if profile == 'monitor':
        filename = os.sep.join(['data', 'monitors.dlt'])
    elif profile == 'jury':
        filename = os.sep.join(['data', 'juries.dlt'])
    if not os.path.exists(filename):
        data = {}
    else:
        data = loadFiles(filename)
    return data, filename

def setPerson(user, profile):
    data, filename = getData(profile)
    error = []
    if len(user) != 3:
        error.append('más datos de los necesarios') 
    if not all([x in ['instrument', 'cedula', 'nombre'] for x in list(user.keys())]):
        error.appen('los key no coinciden')
    if error:
        return str(error)
    cedula = ownModules.formatCedula(user['cedula'])
    nombre = ownModules.formatName(user['nombre'])
    instrumento = ownModules.formatName(user['instrument'])
    data = setData(data, profile, instrumento, cedula, nombre)
    updateFile(data, filename)
    return 'ok'

def updateFile(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def loadFiles(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def setData(data, profile, instrumento, cedula, nombre):
    if profile == 'monitor':
        data[instrumento] = {'cedula': cedula, 'nombre': nombre}
    elif profile == 'jury':
        if data.get(instrumento) is None:
            data[instrumento] = {}
        data[instrumento][nombre] = cedula
    return data

def getListPersons(profile):
    data, filename = getData(profile)
    data = json.dumps(data)
    return data

def removePerson(profile):
    if 'monitor' in profile:
        grupo = profile.replace('monitor', '')
        profile = 'monitor'
        data, filename = getData(profile)
        del data[grupo]
        updateFile(data, filename)
        return
    elif 'jury' in profile:
        profile, grupo, cedula = profile.split('dtl')
        data, filename = getData(profile)
        for nombre in data[grupo]:
            if data[grupo][nombre] == cedula:
                del data[grupo][nombre]
                updateFile(data, filename)
                return

        





