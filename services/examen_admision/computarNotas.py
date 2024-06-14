from pathlib import Path
import requests
import json
import csv


instrGrades = Path.cwd() / 'data' / 'Instrumento_resultados.json'

solfeoGrades = Path.cwd() / 'data' / 'solfeo_resultados_2024_1.json'

teoriaGrades = Path.cwd() / 'data' / 'teoria_result.json'

urlAppTeoria = 'https://riedmusicapp.com/load/get_app_examenua_result/'

masterFile = Path.cwd() / 'data' / 'convocados_archivo_full.csv'

def get_orden_cedulas():
    cedulas_ordenadas = [x.split(',')[1] for x in masterFile.read_text().split('\n')][1:]
    return cedulas_ordenadas

def notas_instrumento():
    instrumentoNotas = json.loads(instrGrades.read_text())
    consolidado = {}
    for cedula, content in instrumentoNotas.items():
        consolidado[cedula] = {}
        for section in ['libre y escalas', 'preparada', 'lectura']:
            if not 'grades' in content:
                consolidado[cedula][section] = 0
                continue
            value = 0
            for jurado in content['grades']:
                try:
                    value += content['grades'][jurado][section]
                except:
                    breakpoint()
            value /= len(content['grades'])
            consolidado[cedula][section] = value
    return consolidado

def notas_solfeo():
    consolidado = json.loads(solfeoGrades.read_text())
    return consolidado

def notas_teoria():
    consolidado = json.loads(teoriaGrades.read_text())
    return consolidado


cedulas = get_orden_cedulas()
instrumento = notas_instrumento()
solfeo = notas_solfeo()
teoria = notas_teoria()

consolidado = ''
for person in cedulas:
    print(person)
    consolidado += person + ','
    if not person in teoria:
        consolidado += '0,0,'
    else:
        for section in ['Teoria', 'AudioPerceptiva']:
            if teoria[person][section]:
                consolidado += f'{teoria[person][section]},'
            else:
                consolidado += '0,'
    if not person in solfeo:
        consolidado += '0,0,'
    else:
        for section in ['lectura_ritmica', 'lectura_melodica']:
            if solfeo[person][section]:
                consolidado += f'{solfeo[person][section]},'
            else:
                consolidado += '0,'
    if not person in instrumento:
        consolidado += '0,0,0,'
    else:
        for section in ['libre y escalas', 'preparada', 'lectura']:
            if instrumento[person][section]:
                consolidado += f'{instrumento[person][section]},'
            else:
                consolidado += '0,'
    consolidado = consolidado[:-1]
    consolidado += '\n'

output = Path.cwd() / 'resultados_para_excel.csv'

output.write_text(consolidado)
