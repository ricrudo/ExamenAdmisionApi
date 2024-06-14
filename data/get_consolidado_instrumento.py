from pathlib import Path
import json

path = Path.cwd()

result = {}
cedulas = {}

for filename in path.iterdir():
    if "GRUPO_" in filename.name:
        cedulas[filename.name] = []
        for cedula, data in json.loads(filename.read_text()).items():
            for grupo in cedulas:
                if cedula in cedulas[grupo]:
                    raise ValueError(f'{cedula} repetida {grupo} y {filename.name}')
            cedulas[filename.name].append(cedula)
            result[cedula] = data

output = Path.cwd() / 'Instrumento_resultados.json'

output.write_text(json.dumps(result, indent=4))

