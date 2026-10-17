from steam.steam_helpers import fetch_shortcuts
from utils.load_data import fetch_config
from pathlib import Path

config = fetch_config()

def replace_launch_cmd_placeholders(launch_cmd, rom_path, retroarch_dir):
    for i in range(len(launch_cmd)):
        if "%ROM_PATH%" in launch_cmd[i]:
            launch_cmd[i] = launch_cmd[i].replace("%ROM_PATH%", rom_path)
        if "%RETROARCH_DIR%" in launch_cmd[i]:
            launch_cmd[i] = launch_cmd[i].replace("%RETROARCH_DIR%", retroarch_dir)

    return launch_cmd

def format_title(rom):
    rom = str(Path(rom).stem)
    return rom.split("(")[0].strip()

def format_launch_cmd(launch_cmd):
    return " ".join(f'"{el}"' for el in launch_cmd)

def get_parent_folder(rom_path):
    return str(Path(rom_path).parent)

def generateShortcut(entry_id, app_id, name, launch_cmd, start_dir):
    return {
            entry_id: {
                "appid": app_id,
                "appname": name,
                "exe": (
                    launch_cmd
                ),
                "StartDir": f'{start_dir}',
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
    entry_counter = 0
    for rom in roms:
        launch_cmds_copy = list(rom["launch_cmd"])
        launch_cmds_copy = replace_launch_cmd_placeholders(launch_cmds_copy, 
                            rom["rom_name"], config["paths"]["retroarch_path"])
        entries.update(generateShortcut(
                        entry_id=str(entry_counter),
                        app_id=0,
                        name=format_title(rom["rom_name"]),
                        launch_cmd=format_launch_cmd(launch_cmds_copy),
                        start_dir=get_parent_folder(rom["rom_name"])
                    ))
        entry_counter += 1
    return entries
