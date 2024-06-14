# setListByInstrument

import json
import os
from datetime import datetime
from database.database import createSession, Candidate

def get_candidate_raw(cedula):
    session = createSession()
    candidates = session.query(Candidate).filter(Candidate.active == True).filter(Candidate.id_person == cedula)
    if not candidates:
        return "No people found"
    response = {}
    response[candidates[0].id_person] = {}
    response[candidates[0].id_person]["name"] = candidates[0].name
    response[candidates[0].id_person]["group"] = candidates[0].group
    session.close()
    return json.dumps(response)
        
def modify_candidate(data):
    session = createSession()
    candidates = session.query(Candidate).filter(Candidate.active == True).filter(Candidate.id_person == data['cedula'])
    if candidates:
        candidate = candidates[0]
    candidate.group = data['grupo']
    session.commit()
    session.close()
    return 'ok'

def set_list_by_instrument(data):
    data = json.loads(data)
    session = createSession()
    for cedula, content in data.items():
        now = datetime.now()
        candidate = Candidate(id_person=cedula,
                              name=content["nombre"],
                              group=content["instrumento"],
                              registration_date=now,
                              active=True,
                              state="inactive",
                              last_change=now,
                              description_last_change="initial registration")
        session.add(candidate)
    session.commit()
    session.close()
    #if not os.path.exists('data'):
    #    os.mkdir('data')
    #filename = os.sep.join(['data', 'list_by_instrument.dlt'])
    #with open(filename, 'w') as f:
    #    json.dump(data, f, indent=4)

    #solfeo = {}

    '''
    for instrument in data:
        filename = os.sep.join(['data', instrument + '.dlt'])
        solfeo |= {key:{'nombre': value, 'lectura_ritmica': '', 'lectura_melodica': '', 'jurado': ''} for key, value in data[instrument].items()}
        newdata = {key:{'nombre': value, 'state':'inactive'} for key, value in data[instrument].items()}
        with open(filename, 'w') as f:
            json.dump(newdata, f, indent=4)
    filename = os.sep.join(['data', 'solfeo.dlt'])
    with open(filename, 'w') as f:
        json.dump(solfeo, f, indent=4)
    '''

