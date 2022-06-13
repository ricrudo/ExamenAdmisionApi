from string import ascii_uppercase

letter = ascii_uppercase + '_() 123456789'

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

def formatCedula(cedula):
    return "".join([x for x in str(cedula) if x.isdigit()])
    pass

def formatName(name):
    return replaceAccents(name)

