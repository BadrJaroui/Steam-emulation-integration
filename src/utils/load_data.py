import json
import toml

def fetch_console_names():
    with open("../config/console_names.json", "r") as file:
        return json.load(file)

def fetch_emulators():
    with open("../config/emulators.json", "r") as file:
        return json.load(file)

def fetch_config():
    with open('../config/config.toml', 'r') as file:
        return toml.load(file)