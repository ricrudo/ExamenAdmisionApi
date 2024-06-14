from flask import Flask, request, render_template, session, url_for, redirect, abort

import ownModules as py

app = Flask(__name__)
app.secret_key = ')s:ie·\xa2]\nr2[\xf2'

dictInstruments = { 'grupo1': 'GRUPO_1',
                    'grupo2': 'GRUPO_2', 
                    'grupo3': 'GRUPO_3', 
                    'grupo4': 'GRUPO_4', 
                    'grupo5': 'GRUPO_5', 
                    'grupo6': 'GRUPO_6', 
                    'grupo7': 'GRUPO_7', 
                    'grupo8': 'GRUPO_8', 
                    'grupo9': 'GRUPO_9', 
                    'grupo10': 'GRUPO_10'
                    }

url_Instrument = {value:key for key, value in dictInstruments.items()}

def check_instrument(instrumento):
    if instrumento not in dictInstruments:
        return 
    return dictInstruments[instrumento]

######################################
#### API APLICACION TEORIA ###########
#### API APLICACION TEORIA ###########
#### API APLICACION TEORIA ###########
#### API APLICACION TEORIA ###########
#### API APLICACION TEORIA ###########
#### API APLICACION TEORIA ###########
######################################

@app.get("/")
def hello_world():
    return "<p>Hello, Worild!</p>"

@app.get("/examen_ua/cuestionario/<institution>")
def get_quest(institution:str):
    # DB montada
    # TODO que reciba tambien el id del estudiante para saber si existe
    data = py.get_cuestionario(institution)
    return data

@app.post("/examen_ua/set_cuestionario")
def set_quest():
    # DB montada
    py.set_cuestionario(request.json)
    return 'ok'

@app.get("/examen_ua/get_results")
def get_results():
    # DB montada
    response = py.getBulkResults(list(dictInstruments.values()))
    return response

@app.post("/examen_ua")
def post_results():
    # DB montada
    py.resultsManager(request.json)
    return 'ok'

@app.post("/examen_ua/suscribe")
def set_suscribers():
    email = request.json    
    py.new_suscriptor(email['email'])
    return 'ok'


#######################################
#### API EXAMEN SOLFEO      ###########
#### API EXAMEN SOLFEO      ###########
#### API EXAMEN SOLFEO      ###########
#### API EXAMEN SOLFEO      ###########
#### API EXAMEN SOLFEO      ###########
#### API EXAMEN SOLFEO      ###########
#######################################


@app.get("/admisionesUA/solfeo_<grupo>/jury")
def jury_getSolfeo(grupo):
    # DB montada
    grupo = f'SOLFEO_{grupo}'
    user = session.get('JURY')
    if user:
        person = py.checkPassword(user, grupo, 'jury')
        if person:
            data = py.solfeoGetCandidates()
            alerta = None
            if request.args:
                selectedCandidate = int(request.args.get("candidate"))
            else:
                selectedCandidate = None
            if request.form:
                return str(request.form)
            return render_template('gradingSolfeo.html', instrumento=grupo, data=data, person=person['nombre'], alerta=alerta, selectedCandidate=selectedCandidate)
    return render_template('login.html', instrumento=grupo)
        
@app.post("/admisionesUA/solfeo_<grupo>/jury")
def jury_postSolfeo(grupo):
    # DB montada sin test
    grupoName = f'SOLFEO_{grupo}'
    person = None
    if 'password' in request.form:
        person = py.checkPassword(request.form['password'], grupoName, 'jury')
        if not person: abort(401)
        session['JURY'] = request.form['password']
        return redirect(url_for('jury_getSolfeo', grupo=grupo))
    if session.get('JURY') is None:
        return redirect(url_for('jury_get', instrumento=url_Instrument[instrumento]))
    if not person:
        person = py.checkPassword(session['JURY'], grupoName, 'jury')
        if not person:
            return redirect(url_for('jury_get', instrumento=url_Instrument[instrumento]))
    if 'candidate' in request.form:
#        with open('test.txt', 'w') as f:
#            f.write(str(request.form))
        py.setGradesSolfeo(request.form, person)
        return 'ok'

#######################################
#### API EXAMEN INSTRUMENTO ###########
#### API EXAMEN INSTRUMENTO ###########
#### API EXAMEN INSTRUMENTO ###########
#### API EXAMEN INSTRUMENTO ###########
#### API EXAMEN INSTRUMENTO ###########
#### API EXAMEN INSTRUMENTO ###########
#######################################

@app.post("/admisionesUA/services/set_list_instrument")
def serviceSetListByInstrument():
    # DB montada
    py.set_list_by_instrument(request.json)
    return 'ok'

@app.get("/admisionesUA/services/get_candidate_<cedula>")
def serviceGetCandidate(cedula):
    # DB montada
    return py.get_candidate_raw(cedula)

@app.post("/admisionesUA/services/modify_candidate")
def modifyCandidate():
    # DB montada
    response = py.modify_candidate(request.json)
    return response

@app.post("/admisionesUA/services/set_monitor")
def serviceSetMonitor():
    # DB montada
    response = py.setPerson(request.json, 'monitor')
    return response

@app.post("/admisionesUA/services/set_jury")
def serviceSetJury():
    # DB montada
    response = py.setPerson(request.json, 'jury')
    return response

@app.get("/admisionesUA/services/getGrades")
def serviceGetGrades():
    # DB montada sin test
    return py.getGrades(list(dictInstruments.values()))

@app.get("/admisionesUA/services/get_<profile>s")
def servicesGetPersons(profile):
    # DB montada
    if not profile in ['monitor', 'jurie']:
        abort(404)
    data = py.getListPersons(profile.replace('ie', 'y')) 
    return data

@app.get("/admisionesUA/services/delete_<profile>")
def servicesDeletePerson(profile):
    # DB montada
    if not any([x in profile for x in ['monitor', 'jury']]):
        abort(404)
    data = py.removePerson(profile) 
    return 'ok'


#### WEBPAGES ######

################################################################
#MONITOR#
#MONITOR#
#MONITOR#
#MONITOR#
#MONITOR#
#MONITOR#
#MONITOR#
################################################################


@app.get("/admisionesUA/<instrumento>/monitor")
def monitor_get(instrumento):
    # DB montada
    instrumento = check_instrument(instrumento)
    if not instrumento: abort(404)
    user = session.get('MONITOR')
    if user:
        person = py.checkPassword(user, instrumento, 'monitor')
        if person:
            data, active = py.getCandidates(instrumento)
            return render_template('monitorDashboard.html', instrumento=instrumento, data=data, active=active, person=person)
    return render_template('login.html', instrumento=instrumento)

@app.post("/admisionesUA/<instrumento>/monitor")
def monitor_post(instrumento):
    # DB montada
    instrumento = check_instrument(instrumento)
    if not instrumento: abort(404)
    person = None
    if 'password' in request.form:
        person = py.checkPassword(request.form['password'], instrumento, 'monitor')
        if not person: abort(401)
        session['MONITOR'] = request.form['password']
        data, active = py.getCandidates(instrumento)
        pendingJuries = False
    if session.get('MONITOR') is None:
        return redirect(url_for('monitor_get', instrumento=url_Instrument[instrumento]))
    if not person:
        person = py.checkPassword(session['MONITOR'], instrumento, 'monitor')
        if not person:
            return redirect(url_for('monitor_get', instrumento=url_Instrument[instrumento]))
    if 'activate' in request.form:
        data = py.activateCandidate(instrumento, request.form['activate'])
        active = True
        pendingJuries = False
    elif 'deactivate' in request.form:
        data, active, pendingJuries = py.deactivateCandidate(instrumento, request.form['deactivate'])
    return render_template('monitorDashboard.html', instrumento=instrumento, data=data, active=active, person=person, pendingJuries=pendingJuries)





################################################################
#JURADO#
#JURADO#
#JURADO#
#JURADO#
#JURADO#
#JURADO#
################################################################

@app.get("/admisionesUA/<instrumento>/jury")
def jury_get(instrumento):
    # DB montada sin test
    instrumento = check_instrument(instrumento)
    if not instrumento: abort(404)
    user = session.get('JURY')
    if user:
        person = py.checkPassword(user, instrumento, 'jury')
        if person:
            data = py.getActiveCandidate(instrumento, person['cedula'])
            alerta = None
            return render_template('grading.html', instrumento=instrumento, data=data, person=person['nombre'], alerta=alerta)
    return render_template('login.html', instrumento=instrumento)

@app.post("/admisionesUA/<instrumento>/jury")
def jury_post(instrumento):
    # DB montada sin test
    instrumento = check_instrument(instrumento)
    if not instrumento: abort(404)
    person = None
    if 'password' in request.form:
        person = py.checkPassword(request.form['password'], instrumento, 'jury')
        if not person: abort(401)
        session['JURY'] = request.form['password']
        data, active = py.getCandidates(instrumento)
        return redirect(url_for('jury_get', instrumento=url_Instrument[instrumento]))
    if session.get('JURY') is None:
        return redirect(url_for('jury_get', instrumento=url_Instrument[instrumento]))
    if not person:
        person = py.checkPassword(session['JURY'], instrumento, 'jury')
        if not person:
            return redirect(url_for('jury_get', instrumento=url_Instrument[instrumento]))
    if 'start' in request.form:
        data = py.getActiveCandidate(instrumento, person['cedula'])
        if not data: alerta = True
        else: alerta = False
        return render_template('grading.html', instrumento=instrumento, data=data, person=person['nombre'], alerta=alerta)
    if 'candidate' in request.form:
        response = py.setGradeCandidate(instrumento, request.form, person['cedula'])
        return 'ok'
    if 'remove' in request.form:
        py.removeJuryAwaiting(instrumento, request.form['remove'], person['cedula'])
        return render_template('grading.html', instrumento=instrumento, data=False, person=person['nombre'], alerta=False)
        
@app.get("/clearsession")
def clearsession():
    session.clear()
    print(session)
    return str(dir(session))
