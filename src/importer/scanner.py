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
    if Path(rom).suffix not in valid_extensions:
        return False
    return True

def is_rom_to_ignore(rom, roms_to_ignore):
    if not roms_to_ignore: return False
    if not rom.suffix == ".m3u":
        for ignored_rom in roms_to_ignore:
            if ignored_rom in str(rom):
                return True
    return False

def format_rom_data(container, rom, emulator_data):
    container.append({"rom_name": str(rom), 
                "emulator_path": emulator_data[1]["path"],
                "launch_cmd": emulator_data[1]["launch_cmd"]})

def scan_folder(rom_dir, roms_to_ignore=None):
    roms_data = []
    emulator_data = get_emulator_from_folder_name(rom_dir)
    if emulator_data is None:
        return None

    for rom in Path(rom_dir).rglob('*'):
        if (is_valid_rom(rom, emulator_data[1]["extensions"]) 
            and not is_rom_to_ignore(rom, roms_to_ignore)):

            format_rom_data(roms_data, rom, emulator_data)
    return roms_data

