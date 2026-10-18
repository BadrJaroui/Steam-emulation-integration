from pathlib import Path
import json
import toml

base_path = Path(__file__).resolve().parent.parent.parent

def fetch_consoles():
    with open(base_path/"config/consoles.json", "r") as file:
        return json.load(file)

def fetch_emulators():
    with open(base_path/"config/emulators.json", "r") as file:
        return json.load(file)

def fetch_config():
    with open(base_path/"config/config.toml", "r") as file:
        return toml.load(file)