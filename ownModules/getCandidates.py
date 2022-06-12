import json
import os
import datetime 

def currentTime():
    current = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
    return current.strftime('%Y-%m-%dT%H:%M:%S')

def getData(instrumento):
    filename = os.sep.join(['data', f'{instrumento}.dlt'])
    with open(filename, 'r') as f:
        return json.load(f)

def getJuries(instrumento):
    filename = os.sep.join(['data', 'juries.dlt'])
    with open(filename, 'r') as f:
        data = json.load(f)
    return data[instrumento]

def setData(instrumento, data):
    if not os.path.exists(os.sep.join(['data', 'backup'])):
        os.mkdir(os.sep.join(['data', 'backup']))
    filename = os.sep.join(['data', 'backup', f'{instrumento}-{currentTime()}.dlt'])
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    filename = os.sep.join(['data', f'{instrumento}.dlt'])
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def getCandidates(instrumento):
    data = getData(instrumento)
    active = False
    for candidate in data:
        if data[candidate]['state'] == 'active':
            active = True
            break
    return data, active
    
def activateCandidate(instrumento,cedula):
    data = getData(instrumento)
    data[cedula]['state'] = 'active'
    setData(instrumento, data)
    return data

def deactivateCadidate(instrumento, aspirante):
    data = getData(instrumento)
    if data[aspirante].get('grades') is None:
        return cleanCandidates(data, instrumento)
    juries = getJuries(instrumento)
    gradedJuries, activeJuries = [], []
    for person, cedula in juries.items():
        if cedula in data[aspirante]['grades']:
            activeJuries.append(person)
            if data[aspirante]['grades'][cedula] != 'awaiting':
                gradedJuries.append(person)
    if len(juries) == len(gradedJuries):
        data[aspirante]['state'] = 'completed'
        return cleanCandidates(data, instrumento)
    else:
        noActivityJuries = [x for x in juries if x not in activeJuries]
        noEndedJuries = [x for x in activeJuries if x not in gradedJuries]
    return data, True, {'noStarted': noActivityJuries, 'noGraded': noEndedJuries}

def cleanCandidates(data, instrumento):
    for candidate in data:
        if data[candidate]['state'] != 'completed': 
            data[candidate]['state'] = 'inactive'
    setData(instrumento, data)
    return data, False, False

def getActiveCandidate(instrumento, person):
    data = getData(instrumento)
    for aspirante in data:
        if data[aspirante]['state'] == 'active':
            if data[aspirante].get('grades') is None:
                data[aspirante]['grades'] = {}

            if not data[aspirante]['grades']:
                data[aspirante]['grades'][person] = 'awaiting'
                setData(instrumento, data)
                return {'cedula':aspirante, 'nombre':data[aspirante]['nombre']}
            
            if person not in data[aspirante]['grades']:
                data[aspirante]['grades'][person] = 'awaiting'
                setData(instrumento, data)
                return {'cedula':aspirante, 'nombre':data[aspirante]['nombre']}
            if data[aspirante]['grades'][person] == 'awaiting':
                return {'cedula':aspirante, 'nombre':data[aspirante]['nombre']}
            else:
                return None
    return None
   
def setGradeCandidate(instrumento, form, jury):
    cedula = form['candidate']
    libre = float(form['libre'])
    escalas = float(form['escalas'])
    preparada = float(form['preparada'])
    lectura = float(form['lectura'])
    grades = {'libre y escalas': (libre + escalas)/2, 'preparada': preparada, 'lectura': lectura}
    data = getData(instrumento)
    if data[cedula]['grades'][jury] == 'awaiting':
        data[cedula]['grades'][jury] = grades
        setData(instrumento, data)
        return
    else: 
        return 'Error'

def removeJuryAwaiting(instrumento, aspirante, jury):
    data = getData(instrumento)
    if data[aspirante].get('grades') is not None:
        data[aspirante]['grades'].pop(jury, None)
        if not data[aspirante]['grades']:
            del data[aspirante]['grades']
    setData(instrumento, data)

def getGrades(instrumentos):
    finalData = {}
    for instrumento in instrumentos:
        data = getData(instrumento)
        for aspirante in data:
            if data[aspirante]['state'] == 'completed':
                finalData[aspirante] = calculateGrade(data[aspirante]['grades'])
            elif data[aspirante]['state'] == 'inactive':
                finalData[aspirante] = {'state': 'inactive','libre y escalas': 0.0, 'preparada': 0.0, 'lectura': 0.0}
            elif data[aspirante]['state'] == 'active':
                finalData[aspirante] = {'state': 'active','libre y escalas': 'en espera', 'preparada': 'en espera', 'lectura': 'en espera'}
    return finalData

def calculateGrade(grades):
    libre = sum([x['libre y escalas'] for x in grades.values()])/len(grades)
    preparada = sum([x['preparada'] for x in grades.values()])/len(grades)
    lectura = sum([x['lectura'] for x in grades.values()])/len(grades)
    return {'state': 'completed','libre y escalas': libre, 'preparada': preparada, 'lectura': lectura}




