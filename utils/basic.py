# OS related functions
import json

def read_json_file(path_like: str) -> dict:
    ''' Read a json file from a given path'''
    with open(path_like, 'r') as f:
        return json.load(f)

