from pathlib import Path
import json
import toml

def fetch_console_names():
    with open("./console_names.json", "r") as file:
        return json.load(file)

def fetch_emulators():
    with open("./emulators.json", "r") as file:
        return json.load(file)

def fetch_config():
    with open('config.toml', 'r') as file:
        return toml.load(file)

config = fetch_config()
console_names = fetch_console_names()
emulators = fetch_emulators()

# read folders and assign emulator based on dict containing possible names (returns dict)
def fetch_folders(roms_dir):
    folders = []
    for pth in Path.iterdir(Path(roms_dir)):
        if not pth.is_dir(): continue
        folders.append((pth.parts[-1]))
    return folders

print(fetch_folders('D:/Emulation/ROMs'))

def assign_emulator(folder_name):
    for console in console_names:
        for name_variant in console_names[console]:
            if folder_name.lower() == name_variant:
                return {f"{config['paths']['roms_path']}/{folder_name}": emulators[console]}
    return {f"{config['paths']['roms_path']}/{folder_name}": None}

# continue to mapper