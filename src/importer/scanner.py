from utils.load_data import fetch_emulators, fetch_consoles
from pathlib import Path

emulators = fetch_emulators()
consoles = fetch_consoles()

def get_console_from_folder_name(rom_dir):
    for console in consoles:
        for name_variant in consoles[console]:
            if Path(rom_dir).parts[-1].lower() == name_variant:
                return console
    return None

def get_emulator_from_folder_name(rom_dir):
    console = get_console_from_folder_name(rom_dir)
    if console is None:
        return None

    for emulator in emulators.items():
        if console == emulator[0]:
            return emulator
    return None

def is_valid_rom(rom, valid_extensions):
    if not Path(rom).is_file():
        return False
    if Path(rom).suffix.replace(".", "") not in valid_extensions:
        return False
    return True

def scan_folder(rom_dir):
    roms_data = []
    emulator_data = get_emulator_from_folder_name(rom_dir)
    if emulator_data is None:
        return None

    for rom in Path.iterdir(Path(rom_dir)):
        if not is_valid_rom(rom, emulator_data[1]["extensions"]):
            continue
        
        roms_data.append({"rom_name": str(rom), 
                          "emulator_path": emulator_data[1]["path"],
                          "launch_cmd": emulator_data[1]["launch_cmd"]})
    return roms_data
