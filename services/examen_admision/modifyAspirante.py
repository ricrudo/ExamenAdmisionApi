import requests

def setConexion():
    dictConexion = {'1': ['local', 'http://127.0.0.1:5000'], '2': ['remota', 'https://riedmusicapp.com/examination']}
    while True:
        print('\nDetermine el tipo de conexión')
        [print(f'{x}- {dictConexion[x][0]}') for x in dictConexion]
        response = input('')
        if response in dictConexion:
            return dictConexion[response][1]

conexion = setConexion()
cedula = input("indique la cedula del aspirante: ")
while True:
    grupo = input("Indique el grupo del aspirante (Unicamente el numero, i.e. 2): ")
    try:
        grupo = int(grupo)
    except ValueError:
        print("valor no valido")
        continue
    if 0 < grupo < 11:
        break
    print("valor no valido")

data = {"cedula":cedula, "grupo": f"GRUPO_{grupo}"}

url = f'{conexion}/admisionesUA/services/modify_candidate'
print(url)
response = requests.post(url=url, json=data)
print(response.status_code)
print(response.text)




