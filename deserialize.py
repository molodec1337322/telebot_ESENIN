import json
from random import randint

def read_data(filename):
    with open(filename, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data