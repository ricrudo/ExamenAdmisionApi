from string import ascii_uppercase

letter = ascii_uppercase + '() '

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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
