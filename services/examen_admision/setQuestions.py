import requests
import json

def setConexion():
    dictConexion = {'1': ['local', 'http://127.0.0.1:5000'], '2': ['remota', 'https://riedmusicapp.com/examination']}
    while True:
        print('\nDetermine el tipo de conexión')
        [print(f'{x}- {dictConexion[x][0]}') for x in dictConexion]
        response = input('')
        if response in dictConexion:
            return dictConexion[response][1]

data = {'institution': 'Promusica',
        'audioperceptiva': {
            'bar': 4,
            'intervals': 4,
            'chords': 4,
            'rhythms': 4,
            'melody': 4,
            'modesScales': 4
            },
        'teoria': {
            'bar': 4,
            'intervals': 4,
            'chords': 4,
            'keys': 4,
            'scales': 4,
            'modesScales': 4
            },
        'time': 30
        }

conexion = setConexion()
url = f'{conexion}/examen_ua/set_cuestionario'
response = requests.post(url, json=data)
print(response.status_code)
print(response.text)

