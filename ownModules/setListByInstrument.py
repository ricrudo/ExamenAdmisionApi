import json
import os

def set_list_by_instrument(data):
    data = json.loads(data)
    filename = os.sep.join(['data', 'list_by_instrument.dlt'])
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    for instrument in data:
        filename = os.sep.join(['data', instrument + '.dlt'])
        newdata = {key:{'nombre': value, 'state':'inactive'} for key, value in data[instrument].items()}
        with open(filename, 'w') as f:
            json.dump(newdata, f, indent=4)

