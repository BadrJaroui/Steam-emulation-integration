from steam.steam_helpers import get_steam_id, fetch_shortcuts
from utils.load_data import fetch_config
import vdf

config = fetch_config()

def add_roms_to_shortcuts(roms):
    d = fetch_shortcuts()
    shortcuts = d["shortcuts"]
    current_id = len(shortcuts)
    app_id = (-99999999 - len(list(shortcuts.keys()))) if shortcuts.keys() else -99999999

    new_roms = {}
    for key in roms:
        new_roms[str(current_id)] = roms[key]
        new_roms[str(current_id)]["appid"] = app_id
        current_id += 1
        app_id -= 1

    shortcuts.update(new_roms)
    return d

def write_to_steam(shortcuts):
    steam_id = get_steam_id()
    vdf.binary_dump(add_roms_to_shortcuts(shortcuts),
                    open(f"{config["paths"]["steam_path"]}/userdata/{steam_id}/config/shortcuts.vdf", "wb"))
