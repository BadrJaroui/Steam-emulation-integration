from utils.load_data import fetch_emulators, fetch_console_names
from pathlib import Path

emulators = fetch_emulators()
console_names = fetch_console_names()

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
