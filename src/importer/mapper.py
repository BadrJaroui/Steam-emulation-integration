from steam.steam_helpers import fetch_shortcuts
from utils.load_data import fetch_config
from pathlib import Path

config = fetch_config()

def replace_placeholders(target, rom_path, retroarch_dir):
    for i in range(len(target)):
        if "%ROM_PATH%" in target[i]:
            target[i] = target[i].replace("%ROM_PATH%", rom_path)
        if "%RETROARCH_DIR%" in target[i]:
            target[i] = target[i].replace("%RETROARCH_DIR%", retroarch_dir)

    return target

def format_title(rom):
    extentionless_rom = str(Path(rom).stem)
    return extentionless_rom.split("(")[0].strip()

def format_target(target):
    return " ".join(f'"{element}"' for element in target)

def get_parent_folder(rom_path):
    return str(Path(rom_path).parent)

def generateShortcut(entryid, appid, name, target, startdir):
    return {
            entryid: {
                "appid": appid,
                "appname": name,
                "exe": (
                    target
                ),
                "StartDir": f'{startdir}',
                "icon": "",
                "ShortcutPath": "",
                "LaunchOptions": "",
                "IsHidden": 0,
                "AllowDesktopConfig": 1,
                "AllowOverlay": 1,
                "OpenVR": 0,
                "Devkit": 0,
                "DevkitGameID": "",
                "DevkitOverrideAppID": 0,
                "LastPlayTime": 0,
                "FlatpakAppID": "",
                "tags": {}
                }
            }

def create_shortcuts(roms: list[dict[str, str, str]]):
    entries = {}
    data = fetch_shortcuts()
    counter = len(data["shortcuts"])
    appid_counter = -99999999
    for rom in roms:
        target_copy = list(rom["emulator_target"])
        target_copy = replace_placeholders(target_copy, rom["rom"], config["paths"]["retroarch_path"])
        entries.update(generateShortcut(
                        entryid=str(counter),
                        appid=appid_counter,
                        name=format_title(rom["rom"]),
                        target=format_target(target_copy),
                        startdir=get_parent_folder(rom["rom"])
                    ))
        counter += 1
        appid_counter -= 1
    return entries
