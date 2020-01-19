import json

def is_json(data):
    try:
        pdata = json.loads(data)
        valid = True
    except ValueError:
        valid = False
    return valid