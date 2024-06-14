import csv
import os
from string import ascii_uppercase
import json
import requests

letter = ascii_uppercase + '_()123456789 '

def setConexion():
    dictConexion = {'1': ['local', 'http://127.0.0.1:5000'], '2': ['remota', 'https://riedmusicapp.com/examination']}
    while True:
        print('\nDetermine el tipo de conexión')
        [print(f'{x}- {dictConexion[x][0]}') for x in dictConexion]
        response = input('')
        if response in dictConexion:
            return dictConexion[response][1]

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

filename = os.sep.join(['data', 'test2.csv'])

with open(filename, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    aspirantes = {row[0]:{'nombre': replaceAccents(row[2]), 'instrumento': replaceAccents(row[1])} for row in spamreader}

instrumentos = {}

for cedula in aspirantes:
    if aspirantes[cedula]['instrumento'] not in instrumentos:
        instrumentos[aspirantes[cedula]['instrumento']] = {}
    instrumentos[aspirantes[cedula]['instrumento']][cedula] = aspirantes[cedula]['nombre']


#data = json.dumps(instrumentos)
data = json.dumps(aspirantes)
conexion = setConexion()
url = f'{conexion}/admisionesUA/services/set_list_instrument'
print(url)
response = requests.post(url=url, json=data)
print(response.status_code)
print(response.text)

