from flask import Flask, request, render_template, session, url_for, redirect, abort

import ownModules as py

app = Flask(__name__)
app.secret_key = ')s:ie·\xa2]\nr2[\xf2'

dictInstruments = { 'bajo': 'BAJO ELECTRICO',
                    'canto': 'CANTO', 
                    'eufonio': 'EUFONIO (BOMBARDINO)',
                    'guitarra_acustica': 'GUITARRA ACUSTICA',
                    'guitarra_electrica': 'GUITARRA ELECTRICA',
                    'percusion': 'PERCUSION',
                    'piano': 'PIANO',
                    'saxofon': 'SAXOFON',
                    'violin': 'VIOLIN',
                    'cello': 'VIOLONCHELO',
                    'trompeta': 'TROMPETA'
                    }

url_Instrument = {value:key for key, value in dictInstruments.items()}

def check_instrument(instrumento):
    if instrumento not in dictInstruments:
        return 
    return dictInstruments[instrumento]

#### API ###########
@app.get("/")
def hello_world():
    return "<p>Hello, Worild!</p>"

@app.get("/examen_ua/cuestionario/<institution>")
def get_quest(institution:str):
    data = py.get_cuestionario(institution)
    return data

@app.post("/examen_ua/set_cuestionario")
def set_quest():
    py.set_cuestionario(request.json)
    return 'ok'

@app.post("/examen_ua")
def get_results():
    py.resultsManager(request.json)
    return 'ok'

@app.post("/examen_ua/suscribe")
def set_suscribers():
    email = request.json    
    py.new_suscriptor(email['email'])
    return 'ok'

@app.post("/admisionesUA/services/set_list_instrument")
def serviceSetListByInstrument():
    py.set_list_by_instrument(request.json)
    return 'ok'

@app.post("/admisionesUA/services/set_monitor")
def serviceSetMonitor():
    response = py.setPerson(request.json, 'monitor')
    return response

@app.post("/admisionesUA/services/set_jury")
def serviceSetJury():
    response = py.setPerson(request.json, 'jury')
    return response

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
    instrumento = check_instrument(instrumento)
    if not instrumento: abort(404)
    person = None
    if 'password' in request.form:
        person = py.checkPassword(request.form['password'], instrumento, 'monitor')
        if not person: abort(401)
        session['MONITOR'] = request.form['password']
        data, active = py.getCandidates(instrumento)
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
        data, active, pendingJuries = py.deactivateCadidate(instrumento, request.form['deactivate'])
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
        
        
