import os
import json
from database.database import createSession, Cuestionario
from datetime import datetime

def set_cuestionario(data):
    if not os.path.exists('institutions'):
        os.mkdir('institutions')
    #filename = os.sep.join(['institutions', data['institution'] + '.dlt'])
    #with open(filename, 'w') as f:
    #    json.dump(data, f, indent=4)
    session = createSession()
    quest = Cuestionario(name_institution=data['institution'], content=json.dumps(data), date=datetime.now())
    session.add(quest)
    session.commit()
    session.close()
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
    session = createSession()
    results = session.query(Cuestionario).filter(Cuestionario.name_institution == institution).order_by(Cuestionario.id_cuestionario.desc()).first()
    session.close()
    if results:
        return json.loads(results.content)
    return 'NotFound'
    #filename = os.sep.join(['institutions', institution + '.dlt'])
    #print(filename)
    #if os.path.exists(filename):
    #    with open(filename, 'r') as f:
    #        return json.load(f)
    #return 'NotFound'
