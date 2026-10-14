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

def get_console(folder_dir):
    for console in console_names:
        for name_variant in console_names[console]:
            if Path(folder_dir).parts[-1].lower() == name_variant:
                return console
    return None

def get_emulator_from_folder_name(folder_dir):
    console = get_console(folder_dir)
    if console is None:
        return

    for emulator in emulators.items():
        if emulator[0] == console:
            return emulator
    return None

def scan_folder(rom_folder):
    roms_data = []
    emulator_data = get_emulator_from_folder_name(rom_folder)
    if emulator_data is None:
        return

    for rom in Path.iterdir(Path(rom_folder)):
        if not rom.is_file(): continue
        if str(rom).split(".")[-1] not in emulator_data[1]["extensions"]: continue
        
        roms_data.append({"rom": str(rom), 
                          "emulator_path": emulator_data[1]["path"],
                          "emulator_target": emulator_data[1]["target"]})

    return roms_data

# continue to mapper