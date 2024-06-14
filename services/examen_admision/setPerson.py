# Este modulo permite adjudicar jurados a los grupos

import requests
from formatData import formatCedula, formatName, bcolors
import os
import json
from datetime import datetime
from pathlib import Path
import csv
from string import ascii_uppercase

dictInstruments = {f'{x}':f'GRUPO_{x}' for x in range(1, 11)} 
dictInstruments |= {f'{x}':f'SOLFEO_{x}' for x in range(11, 21)}

letter = ascii_uppercase + '_()123456789 '

opcionPerson = {'1': 'monitor', '2': 'jurado'}

JURIES_BULK = Path.cwd() / 'data' / 'lista_jurados.csv'

def replaceAccents(data):
    data = data.upper().strip()
    data = data.replace('Á', 'A')
    data = data.replace('É', 'E')
    data = data.replace('Í', 'I')
    data = data.replace('Ó', 'O')
    data = data.replace('Ú', 'U')
    data = data.replace('Ñ', 'N')
    response = ''
    for car in data:
        if car in letter:
            response += car
        else:
            response += '_'
    return response

def setConexion():
    dictConexion = {'1': ['local', 'http://127.0.0.1:5000'], '2': ['remota', 'https://riedmusicapp.com/examination']}
    while True:
        print('\nDetermine el tipo de conexión')
        [print(f'{x}- {dictConexion[x][0]}') for x in dictConexion]
        response = input('')
        if response in dictConexion:
            return dictConexion[response][1]

def runSetPerson(profile):
    os.system('clear')
    print(f'{bcolors.BOLD}INGRESO NUEVO {profile.upper()}')
    while True:
        nombre = formatName(input(f'\n{bcolors.ENDC}Ingrese el nombre del {profile}:\n-- '))
        if nombre:
            break
        print(f'{bcolors.WARNING}No ha ingresado el nombre{bcolors.ENDC}')

    while True:
        cedula = formatCedula(input(f'\nIngrese el número de cédula del {profile}:\n-- '))
        if cedula:
            break
        print(f'{bcolors.WARNING}Ha ingresado un número no válido{bcolors.ENDC}')


    [print(f'{key}- {value}') for key, value in dictInstruments.items()]
    while True:
        instrumento = input('\nSeleccione el instrumento indicando el número que lo representa:\n-- ')
        if instrumento.strip() in dictInstruments:
            break
        print('{bcolors.WARNING}ERROR: Opción no válida{bcolors.ENDC}')

    nombre = formatName(nombre)
    instrumento = dictInstruments[instrumento]

    while True:
        print('\n')
        print('Confirme los datos:')
        print(f'{bcolors.OKGREEN}Actividad: {bcolors.ENDC}{profile}\n{bcolors.OKGREEN}Nombre: {bcolors.ENDC}{nombre}\n{bcolors.OKGREEN}Cédula: {bcolors.ENDC}{cedula}\n{bcolors.OKGREEN}Instrumento: {bcolors.ENDC}{instrumento}')
        confirmacion = input('y/n: ').strip().lower()
        if confirmacion == 'y':
            break
        if confirmacion == 'n':
            return

    data = {
            'cedula': cedula,
            'nombre': nombre,
            'instrument': instrumento
            }
    
    if profile == 'jurado': profile = 'jury'

    conexion = setConexion()
    url = f'{conexion}/admisionesUA/services/set_{profile}'
    print(url)

    response = requests.post(url=url, json=data)
    if response.status_code != 200:
        print(response.text)
        print(f'{bcolors.FAIL}Ha ocurrido un error. Por favor revise el log anterior{bcolors.ENDC}')
        input()

def formatGrades(grades):
    data = json.loads(grades)
    for aspirante in data:
        if data[aspirante]['state'] == 'completed':
            print(f'{bcolors.OKGREEN}', end='')
        elif data[aspirante]['state'] == 'active':
            print(f'{bcolors.WARNING}', end='')
        else:
            print(f'{bcolors.FAIL}', end='')
        print(f'\n{aspirante}')
        print(f'    Obra libre y escalas: {data[aspirante]["libre y escalas"]}\n    Obra preparada: {data[aspirante]["preparada"]}\n    lectura: {data[aspirante]["lectura"]}\n')
        print(f'{bcolors.ENDC}', end='')
    input('\n\n\n presione Enter para continuar')
    os.system('clear')


def getGrades(upload=None, printOnScreen=True):
    conexion = setConexion()
    url = f'{conexion}/admisionesUA/services/getGrades'
    print(url)

    response = requests.get(url=url)
    if response.status_code == 200:
        if not upload:
            if printOnScreen:
                formatGrades(response.text)
            else:
                return response.text
    else:
        print(response.text)
        print(f'{bcolors.FAIL}Ha ocurrido un error. Por favor revise el log anterior{bcolors.ENDC}')
        input()

def saveGradesToFile():
    data = json.loads(getGrades(printOnScreen=False))

    filename = Path.cwd() / "data" / f"Instrumento_resultados_{datetime.now().strftime('%d-%m-%Y')}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'Archivo guardado "{filename}"')
    input('\n\n\n presione Enter para continuar')
    os.system('clear')
    

def getListPerson(profile):
    conexion = setConexion()
    url = f'{conexion}/admisionesUA/services/get_{profile}'
    print(url)
    response = requests.get(url=url)
    if response.status_code != 200:
        print(response.text)
        print(f'{bcolors.FAIL}Ha ocurrido un error. Por favor revise el log anterior{bcolors.ENDC}')
        input()
        return
    return json.loads(response.text), conexion


def removeMonitor():
    data, conexion = getListPerson('monitors')
    data = createListPeople(data)
    while True:
        for index, content in enumerate(data, 1):
            print(f"{index} - {content}")
        response = input('Indique el grupo de que quiere eliminar al monitor: ')
        try:
            response = int(response)
        except ValueError:
            print("valor no valido")
            continue
        if 0 < response <= len(data):
            response -= 1
            break
        print("valor no valido")
    url = f'{conexion}/admisionesUA/services/delete_monitor{data[response]["group"]}'
    response = requests.get(url=url)
    if response.status_code != 200:
        print(response.text)
        print(f'{bcolors.FAIL}Ha ocurrido un error. Por favor revise el log anterior{bcolors.ENDC}')
        input()

def removeJury():
    data, conexion = getListPerson('juries')
    data = createListPeople(data)
    while True:
        for index, content in enumerate(data, 1):
            print(f"{index} - {content}")
        response = input('Indique el grupo de que quiere eliminar al jurado: ')
        try:
            response = int(response)
        except ValueError:
            print("valor no valido")
            continue
        if 0 < response <= len(data):
            response -= 1
            break
        print("valor no valido")
    url = f'{conexion}/admisionesUA/services/delete_jurydtl{data[response]["group"]}dtl{data[response]["cedula"]}'
    response = requests.get(url=url)
    if response.status_code != 200:
        print(response.text)
        print(f'{bcolors.FAIL}Ha ocurrido un error. Por favor revise el log anterior{bcolors.ENDC}')
        input()

def createListPeople(data):
    newData = []
    for cedula, content in data.items():
        content = {"cedula":cedula, "nombre": content['name'], "group":content["group"]}
        newData.append(content)
    return newData

def addJuriesBulk():
    with open(JURIES_BULK, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = {}
        for row in spamreader:
            if row:
                if row[0] not in data:
                    data[row[0]] = []
                data[row[0]].append((replaceAccents(row[1]), row[2]))
    for grupo, persons in data.items():
        for person in persons:
            pack = {
                    'cedula': person[1],
                    'nombre': person[0],
                    'instrument': grupo
                    }
            
            conexion = setConexion()
            url = f'{conexion}/admisionesUA/services/set_jury'
            print(url)

            response = requests.post(url=url, json=pack)
            if response.status_code != 200:
                print(response.text)
                print(f'{bcolors.FAIL}Ha ocurrido un error. Por favor revise el log anterior{bcolors.ENDC}')
                input()



def otherOptions():
    os.system('clear')
    print(f'{bcolors.BOLD}OTRAS OPCIONES{bcolors.ENDC}')
    optionsFunc = {'1': getGrades, '2': saveGradesToFile, '3': removeMonitor, '4': removeJury, '5': addJuriesBulk}
    options = {'1': 'Obtener Notas Instrumento', '2': 'Guardar las notas en un archivo JSON', '3': 'Eliminar monitor', '4': 'Eliminar jurado', '5': 'Agregar los jurados desde un archivo'}
    [print(f'{key}- {value}') for key, value in options.items()]
    while True:
        opcion = input('Seleccione una opción indicando el número que lo representa:\n-- ')
        if opcion.strip() in options:
            optionsFunc[opcion]()
            break


while True:
    os.system('clear')
    print(f'{bcolors.BOLD}¿Que desea hacer?{bcolors.ENDC}\n')
    [print(f'{key}- Ingresar un nuevo {value}') for key, value in opcionPerson.items()]
    print(f'{len(opcionPerson) + 1}- Otro')
    while True:
        opcion = input('Seleccione una opción indicando el número que lo representa:\n-- ')
        if opcion.strip() in opcionPerson:
            runSetPerson(opcionPerson[opcion])
            break
        if opcion.strip() == str(len(opcionPerson)+1):
            print('Otras opciones aun no ahabilitadas, pero cada se podrá escoger ver monitores registrados, ver jurados registrados, eliminar jurado, eliminar monitor, ver avance de completados por instrumento, ver calificaciones')
            otherOptions()
            break
        print('{bcolors.WARNING}ERROR: Opción no válida{bcolors.ENDC}')

