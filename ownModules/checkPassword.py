# checkPassword

import json
import os
import datetime
from database.database import createSession, Person

def currentTime():
    current = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
    return current.strftime('%Y-%m-%dT%H:%M:%S')

def checkPassword(password, instrumento, profile):
    session = createSession()
    #if profile == 'monitor':
    #    filename = os.sep.join(['data', 'monitors.dlt'])
    #elif profile == 'jury':
    #    filename = os.sep.join(['data', 'juries.dlt'])
    #with open(filename, 'r') as f:
    #    data = json.load(f)
    persons = session.query(Person).filter(Person.active == True).filter(Person.id_person == password).filter(Person.role == profile)
    if not persons:
        return False
    person = persons[0]
    if profile == 'monitor':
        response = person.name
    elif profile == 'jury':
        response = {'cedula':person.id_person, 'nombre': person.name}
    createPersonLog(password)
    session.close()
    return response

    #response = False
    #if profile == 'monitor' and data[instrumento]['cedula'] == password:
    #    response = data[instrumento]['nombre']
    #elif profile == 'jury':
    #    for person, cedula in data[instrumento].items():
    #        if cedula == password:
    #            response = {'cedula':cedula, 'nombre': person}
    #            break
    #createPersonLog(password)
    #return response

def createPersonLog(cedula):
    filename = os.sep.join(['data', 'personalLog'])
    if not os.path.exists(filename):
        os.mkdir(filename)
    filename = os.sep.join(['data', 'personalLog', 'monitors.dlt'])
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('{}')

def checkIdStudent(password):
    filename = os.sep.join(['data', 'list_by_instrument.dlt'])
    with open(filename, 'r') as f:
        data = json.load(f)
    for instrumento in data.values():
        if password in instrumento:
            return True
    return False



