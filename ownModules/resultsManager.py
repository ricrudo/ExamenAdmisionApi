import json
import os
import ownModules as py
from datetime import datetime
from database.database import createSession, AudioTeoriaBD, Candidate

def resultsManager(data):
    pointsAudioP = calculate_score(data['audioperceptiva'])
    pointsTeoria = calculate_score(data['teoria'])
    save_data(data, pointsAudioP, pointsTeoria)
    save_general_users(data['nombre'], data['cedula'], pointsAudioP, pointsTeoria)

def calculate_score(data):
    score = [0,0]
    for topic in data.keys():
        for question in data[topic].keys():
            if 'points' in data[topic][question]:
                score[0] += data[topic][question]['points']
            score[1] += 1
    return score

def save_data(data, pointsAudioP, pointsTeoria):
    if not os.path.exists('users'):
        os.mkdir('users')
    filename = os.sep.join(['users', data['cedula'] + '.dlt'])
    data = {'nombre':data['nombre'], 'cedula':data['cedula'],\
            'audioperceptiva':data['audioperceptiva'],\
            'teoria':data['teoria'],\
            'Head':data['Head'],\
            'left_time':data['left_time'],\
            'points_audioperceptiva':f'{pointsAudioP[0]}/{pointsAudioP[1]}',\
            'points_teoria':f'{pointsTeoria[0]}/{pointsTeoria[1]}'}
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def save_general_users(nombre, cedula, pointsAudioP, pointsTeoria):
    pointsAudioP = get_grade(pointsAudioP)
    pointsTeoria = get_grade(pointsTeoria)
    session = createSession()
    data = AudioTeoriaBD(id_estudiante=cedula,
                         audioperceptiva=float(pointsAudioP),
                         teoria=float(pointsTeoria),
                         date=datetime.now(),
                         active=True)
    session.add(data)
    session.commit()
    session.close()
    #filename = os.sep.join(['users', 'general.dlt'])
    #if os.path.exists(filename):
    #    with open(filename, 'r') as f:
    #        data = json.load(f)
    #else:
    #    data = {}
    #data[cedula] = {'nombre': nombre, 'AudioPerceptiva': float(pointsAudioP), 'Teoria': float(pointsTeoria)}
    #with open(filename, 'w') as f:
    #    json.dump(data, f, indent=4)

def get_grade(score):
    return f'{(int(score[0])*5)/int(score[1]):.1f}'

def getBulkResults(listInstrumentos):
    #cedulas = [f'{j}.dlt' for x in listInstrumentos for j in list(py.getCandidates(x)[0].keys())]
    poolResult = {}
    session = createSession()
    resultsCandidate = session.query(Candidate).filter(Candidate.active == True)
    for person in resultsCandidate:
        if not person.id_person in poolResult:
            poolResult[person.id_person] = {}
        poolResult[person.id_person]['grades_instrumento'] = person.grades_instrument
        poolResult[person.id_person]['grades_solfeo'] = person.grades_solfeo
    resultsAudioTeoria = session.query(AudioTeoriaBD).filter(AudioTeoriaBD.active == True)
    for person in resultsAudioTeoria:
        if not person.id_estudiante in poolResult:
            poolResult[person.id_estudiante] = {}
        poolResult[person.id_estudiante]["audioperceptiva"] = person.audioperceptiva
        poolResult[person.id_estudiante]["teoria"] = person.teoria
    #for person in cedulas:
    #    filename = os.sep.join(['users', person])
    #    if not os.path.exists(filename):
    #        continue
    #    with open(filename, 'r') as f:
    #        data = json.load(f)
    #    poolResult[data['cedula']] = {}
    #    poolResult[data['cedula']]['audioperceptiva'] = calculateGradein5(data['points_audioperceptiva'])
    #    poolResult[data['cedula']]['teoria'] = calculateGradein5(data['points_teoria'])
    session.close()
    return json.dumps(poolResult)


def calculateGradein5(value):
    breakpoint()
    points, total = value.split('/')
    return int(points) * 5 / int(total)









