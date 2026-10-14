import toml
from pathlib import Path
import vdf

def fetch_config():
    with open('config.toml', 'r') as file:
        return toml.load(file)
config = fetch_config()

def read_data():
    if not Path.exists(Path(f"{config["paths"]["steam_path"]}/userdata/{get_steam_id()}/config/shortcuts.vdf")):
        vdf.binary_dump({"shortcuts": {}}, open(f'{config["paths"]["steam_path"]}/userdata/{get_steam_id()}/config/shortcuts.vdf', 'wb'))
    with open(f"{config["paths"]["steam_path"]}/userdata/{get_steam_id()}/config/shortcuts.vdf", "rb") as f:
        data = vdf.binary_loads(f.read())
        if not any(data):
            data["shortcuts"] = {}
    return data

def convert_steam64_to_steam3(steam64):
    offset = 76561197960265728
    return steam64 - offset

def read_users_file():
    users_file = f"{config["paths"]["steam_path"]}\\config\\loginusers.vdf"
    with open(users_file) as f:
        return vdf.load(f)

def get_steam_id():
    users = read_users_file()
    for item in users:
        for user_id in users[item]:
            if users[item][user_id]['AutoLogin'] == "1":
                return convert_steam64_to_steam3(int(user_id))

# take folder path and core/emulator, iterate over files and create vdf-formatted entries

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
    data = read_data()
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

# pass entries to writer