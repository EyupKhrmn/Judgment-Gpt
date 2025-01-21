import json

def JsonSerialize(data):
    serialize = json.dumps(data, indent=4, ensure_ascii=False)
    return serialize