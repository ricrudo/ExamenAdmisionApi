import json
import os
import ownModules
from datetime import datetime
from database.database import createSession, Person

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
    #data, filename = getData(profile)
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
    session = createSession()
    person = Person(id_person=cedula, name=nombre, group=instrumento, date=datetime.now(), role=profile, active=True)
    session.add(person)
    session.commit()
    session.close()
    #data = setData(data, profile, instrumento, cedula, nombre)
    #updateFile(data, filename)
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
    session = createSession()
    persons = session.query(Person).filter(Person.role==profile).filter(Person.active==True)
    data = {}
    for person in persons:
        data[person.id_person] = {"name":person.name, "group":person.group}        
    #data, filename = getData(profile)
    session.close()
    return json.dumps(data)

def removePerson(profile):
    if 'monitor' in profile:
        session = createSession()
        grupo = profile.replace('monitor', '')
        persons = session.query(Person).filter(Person.role=="monitor").filter(Person.group == grupo)
        if not persons:
            return "person not found"
        for person in persons:
            person.active = False
        session.commit()
        #profile = 'monitor'
        #
        #data, filename = getData(profile)

        #del data[grupo]
        #updateFile(data, filename)
        session.close()
        return "ok"
    elif 'jury' in profile:
        session = createSession()
        profile, grupo, cedula = profile.split('dtl')
        persons = session.query(Person).filter(Person.role=="jury").filter(Person.group == grupo).filter(Person.id_person == cedula)
        for person in persons:
            person.active = False
        session.commit()
        session.close()
        return "ok"
        #data, filename = getData(profile)
        #for nombre in data[grupo]:
        #    if data[grupo][nombre] == cedula:
        #        del data[grupo][nombre]
        #        updateFile(data, filename)
        #        return

