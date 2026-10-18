from pathlib import Path
import json
import toml

def fetch_consoles():
    with open(Path(Path.cwd()/"config/consoles.json"), "r") as file:
        return json.load(file)

def fetch_emulators():
    with open(Path.cwd()/"config/emulators.json", "r") as file:
        return json.load(file)

def fetch_config():
    with open(Path.cwd()/"config/config.toml", "r") as file:
        return toml.load(file)