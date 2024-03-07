import json

def Encode(**kwargs):
    try:
        return json.dumps(kwargs).encode("utf-8")
    except:
        return {}

def Decode(data):
    try:
        return json.loads(data.decode("utf-8"))
    except:
        return {}