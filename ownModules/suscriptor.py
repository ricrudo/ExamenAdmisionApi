import os

def new_suscriptor(email):
    if not os.path.exists('suscriptors'):
        os.mkdir('suscriptors')
    filename = os.sep.join(['suscriptors', 'suscriptors.dlt'])
    if not os.path.exists(filename):
        modeWrite = 'w'
    else:
        modeWrite = 'a'
    with open(filename, modeWrite) as f:
        f.write(email + '\n')
