import json
import os

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
    filename = os.sep.join(['users', 'general.dlt'])
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    data[cedula] = {'nombre': nombre, 'AudioPerceptiva': float(pointsAudioP), 'Teoria': float(pointsTeoria)}
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_grade(score):
    return f'{(int(score[0])*5)/int(score[1]):.1f}'



