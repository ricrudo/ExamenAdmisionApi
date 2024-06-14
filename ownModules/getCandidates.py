import json
import os
import datetime 
from database.database import createSession, Candidate, Person

def currentTime():
    current = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
    return current.strftime('%Y-%m-%dT%H:%M:%S')

def getData(instrumento, jsonFormat=False):
    session = createSession()
    candidates = session.query(Candidate).filter(Candidate.active == True).filter(Candidate.group == instrumento)
    if jsonFormat:
        candidates = setJsonFormat(candidates)
        session.close()
        return candidates
    return session, candidates

def setJsonFormat(candidates):
    response = {}
    for candidate in candidates:
        response[candidate.id_person] = {}
        response[candidate.id_person]["nombre"] = candidate.name
        response[candidate.id_person]["state"] = candidate.state
        if candidate.grades_instrument:
            response[candidate.id_person]["grades"] = json.loads(candidate.grades_instrument)
    return response
    #filename = os.sep.join(['data', f'{instrumento}.dlt'])
    #with open(filename, 'r') as f:
    #    return json.load(f)

def getJuries(instrumento):
    session = createSession()
    persons = session.query(Person).filter(Person.active == True).filter(Person.role == 'jury').filter(Person.group == group)
    response = {}
    session.close()
    for person in persons:
        response[person.group][person.name] = person.id_person 
    session.close()
    return response
    #filename = os.sep.join(['data', 'juries.dlt'])
    #with open(filename, 'r') as f:
    #    data = json.load(f)
    #return data[instrumento]

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
    data = getData(instrumento, jsonFormat=True)
    active = False
    for candidate in data:
        if data[candidate]['state'] == 'active':
            active = True
            break
    return data, active
    
def activateCandidate(instrumento, cedula):
    session = createSession()
    person = session.query(Candidate).filter(Candidate.active == True).filter(Candidate.id_person == cedula).first()
    person.state = "active"
    session.commit()
    session.close()
    data = getData(instrumento, jsonFormat=True)
    #data[cedula]['state'] = 'active'
    #setData(instrumento, data)
    return data

def deactivateCandidate(instrumento, aspirante):
    session = createSession()
    data = session.query(Candidate).filter(Candidate.active == True).filter(Candidate.id_person == aspirante)
    if not data:
        return "Person not found"
    data = data[0]
    if not data.grades_instrument:
        return cleanCandidates(data, instrumento)
    grades_instrument = json.loads(data.grades_instrument)
    juries = getJuries(instrumento)
    gradedJuries, activeJuries = [], []
    for person, cedula in juries.items():
        if cedula in grades_instrument:
            activeJuries.append(person)
            if grades_instrument[cedula] != 'awaiting':
                gradedJuries.append(person)
    if len(juries) == len(gradedJuries):
        data.state = 'completed'
        session.commit()
        session.close()
        return cleanCandidates(data, instrumento)
    else:
        noActivityJuries = [x for x in juries if x not in activeJuries]
        noEndedJuries = [x for x in activeJuries if x not in gradedJuries]
    session.close()
    data = getData(instrumento, jsonFormat=True)
    return data, True, {'noStarted': noActivityJuries, 'noGraded': noEndedJuries}
    #data = getData(instrumento)
    #if data[aspirante].get('grades') is None:
    #    return cleanCandidates(data, instrumento)
    #juries = getJuries(instrumento)
    #gradedJuries, activeJuries = [], []
    #for person, cedula in juries.items():
    #    if cedula in data[aspirante]['grades']:
    #        activeJuries.append(person)
    #        if data[aspirante]['grades'][cedula] != 'awaiting':
    #            gradedJuries.append(person)
    #if len(juries) == len(gradedJuries):
    #    data[aspirante]['state'] = 'completed'
    #    return cleanCandidates(data, instrumento)
    #else:
    #    noActivityJuries = [x for x in juries if x not in activeJuries]
    #    noEndedJuries = [x for x in activeJuries if x not in gradedJuries]
    #return data, True, {'noStarted': noActivityJuries, 'noGraded': noEndedJuries}

def cleanCandidates(data, instrumento):
    session = createSession()
    candidates = session.query(Candidate).filter(Candidate.active == True).filter(Candidate.group == instrumento)
    for candidate in candidates:
        if candidate.state != 'completed': 
            candidate.stat = 'inactive'
    session.commit()
    session.close()
    data = getData(instrumento, jsonFormat=True)
    #for candidate in data:
    #    if data[candidate]['state'] != 'completed': 
    #        data[candidate]['state'] = 'inactive'
    #setData(instrumento, data)
    return data, False, False

def getActiveCandidate(instrumento, person):
    session, candidates = getData(instrumento)
    for candidate in candidates:
        if candidate.state == "active":
            if not candidate.grades_instrument:
                grades_instrument = {}
            else:
                grades_instrument = json.loads(candidate.grades_instrument)
            if not grades_instrument or person not in grades_instrument:
                grades_instrument[person] = 'awaiting'
                candidate.grades_instrument = json.dumps(grades_instrument)
                session.commit()
                cedula = candidate.id_person
                nombre = candidate.name
                session.close()
                return {'cedula':cedula, 'nombre':nombre}
            if grades_instrument[person] == "awaiting":
                cedula = candidate.id_person
                nombre = candidate.name
                session.close()
                return {'cedula':cedula, 'nombre':nombre}
            else:
                session.close()
                return None
    session.close()
    return None
    #for aspirante in data:
    #    if data[aspirante]['state'] == 'active':
    #        if data[aspirante].get('grades') is None:
    #            data[aspirante]['grades'] = {}

    #        if not data[aspirante]['grades']:
    #            data[aspirante]['grades'][person] = 'awaiting'
    #            setData(instrumento, data)
    #            return {'cedula':aspirante, 'nombre':data[aspirante]['nombre']}
    #        
    #        if person not in data[aspirante]['grades']:
    #            data[aspirante]['grades'][person] = 'awaiting'
    #            setData(instrumento, data)
    #            return {'cedula':aspirante, 'nombre':data[aspirante]['nombre']}
    #        if data[aspirante]['grades'][person] == 'awaiting':
    #            return {'cedula':aspirante, 'nombre':data[aspirante]['nombre']}
    #        else:
    #            return None
    #return None
   
def setGradeCandidate(instrumento, form, jury):
    cedula = form['candidate']
    libre = float(form['libre'])
    escalas = float(form['escalas'])
    preparada = float(form['preparada'])
    lectura = float(form['lectura'])
    grades = {'libre y escalas': (libre + escalas)/2, 'preparada': preparada, 'lectura': lectura}
    session = createSession()
    candidate = session.query(Candidate).filter(Candidate.active == True).filter(Candidate.id_person == cedula)
    if not candidate:
        session.close()
        return "Person not found"
    candidate = candidate[0]
    grades_instrument = json.loads(candidate.grades_instrument)
    if grades_instrument[jury] == 'awaiting':
        grades_instrument[jury] = grades
        candidate.grades_instrument = json.dumps(grades_instrument)
        session.commit()
        session.close()
        return
    else:
        session.close()
        return 'Error'

    #if data[cedula]['grades'][jury] == 'awaiting':
    #    data[cedula]['grades'][jury] = grades
    #    setData(instrumento, data)
    #    return
    #else: 
    #    return 'Error'

def removeJuryAwaiting(instrumento, aspirante, jury):
    session = createSession()
    candidate = session.query(Candidate).filter(Candidate.active == True).filter(Candidate.id_person == cedula)
    if not candidate:
        session.close()
        return "Person not found"
    candidate = candidate[0]
    if candidate.grades_instrument:
        grades_instrument = json.loads(candidate.grades_instrument)
        grades_instrument.pop(jury, None)
        if not grades_instrument:
            grades_instrument = None
        candidate.grades_instrument = json.dumps(grades_instrument)
        session.commit()
        session.close()

    #data = getData(instrumento)
    #if data[aspirante].get('grades') is not None:
    #    data[aspirante]['grades'].pop(jury, None)
    #    if not data[aspirante]['grades']:
    #        del data[aspirante]['grades']
    #setData(instrumento, data)

def getGrades(instrumentos):
    session = createSession()
    candidates = session.query(Candidate).filter(Candidate.active == True)
    finalData = {}
    for person in candidates:
        if person.state == "completed":
            finalData[person.id_person] = calculateGrade(json.loads(person.grades_instrument))
        elif person.state == 'inactive':
            finalData[person.id_person] = {'state': 'inactive','libre y escalas': 0.0, 'preparada': 0.0, 'lectura': 0.0}
        elif person.state == 'active':
            finalData[person.id_person] = {'state': 'active','libre y escalas': 'en espera', 'preparada': 'en espera', 'lectura': 'en espera'}
        if person.grades_solfeo:
            finalData[person.id_person]["solfeo"] = json.loads(person.grades_solfeo)
    session.close()
    return finalData
    #for instrumento in instrumentos:
    #    data = getData(instrumento)
    #    for aspirante in data:
    #        if data[aspirante]['state'] == 'completed':
    #            finalData[aspirante] = calculateGrade(data[aspirante]['grades'])
    #        elif data[aspirante]['state'] == 'inactive':
    #            finalData[aspirante] = {'state': 'inactive','libre y escalas': 0.0, 'preparada': 0.0, 'lectura': 0.0}
    #        elif data[aspirante]['state'] == 'active':
    #            finalData[aspirante] = {'state': 'active','libre y escalas': 'en espera', 'preparada': 'en espera', 'lectura': 'en espera'}
    #return finalData

def calculateGrade(grades):
    libre = sum([x['libre y escalas'] for x in grades.values()])/len(grades)
    preparada = sum([x['preparada'] for x in grades.values()])/len(grades)
    lectura = sum([x['lectura'] for x in grades.values()])/len(grades)
    return {'state': 'completed','libre y escalas': libre, 'preparada': preparada, 'lectura': lectura}




