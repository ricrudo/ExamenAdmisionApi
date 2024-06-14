# getCandidatesSolfeo

import json
from pathlib import Path
import datetime 
from database.database import createSession, Candidate

def solfeoGetCandidates():
    session = createSession()
    candidates = session.query(Candidate).filter(Candidate.active==True)
    data = {}
    for candidate in candidates:
        if not candidate.grades_solfeo:
            data[candidate.id_person] = {}
            data[candidate.id_person]["nombre"] = candidate.name
            data[candidate.id_person]["lectura_ritmica"] = ""
            data[candidate.id_person]["lectura_melodica"] = ""
            data[candidate.id_person]["jurado"] = ""
    session.close()
    return data

    #candidatesPath = Path.cwd() / 'data' / 'solfeo.dlt'
    #with open(candidatesPath) as f:
    #    return json.load(f)

def setGradesSolfeo(form, jury):
    session = createSession()
    candidate = session.query(Candidate).filter(Candidate.active == True).filter(Candidate.id_person==form['candidate']).first()
    if not candidate:
        return "Person not found"
    data = {}
    data['lectura_ritmica'] = form['ritmica']
    data['lectura_melodica'] = form['melodica']
    data['jurado'] = jury['nombre']
    data = json.dumps(data)
    candidate.grades_solfeo = data
    session.commit()
    session.close()
    return "ok"

    #candidatesPath = Path.cwd() / 'data' / 'solfeo.dlt'
    #with open(candidatesPath) as f:
    #    data = json.load(f)
    #cedula = form['candidate']
    #if cedula in data:
    #    data[cedula]['lectura_ritmica'] = form['ritmica']
    #    data[cedula]['lectura_melodica'] = form['melodica']
    #    data[cedula]['jurado'] = jury['nombre']
    #    with open(candidatesPath, 'w') as f:
    #        json.dump(data, f, indent=4)   
    
