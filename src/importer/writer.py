from steam.steam_helpers import get_steam_id, fetch_shortcuts
from utils.load_data import fetch_config
import vdf

config = fetch_config()

def rom_exists(shortcuts, new_rom):
    for key in shortcuts:
        if shortcuts[key]["exe"] == new_rom["exe"]:
            return True
    return False

def get_corrected_roms(roms):
    d = fetch_shortcuts()
    shortcuts = d["shortcuts"]
    current_id = len(shortcuts)
    app_id = (shortcuts[list(shortcuts.keys())[-1]]["appid"] - 1) if shortcuts.keys() else -99999999

    new_roms = {}
    for key in roms:
        if rom_exists(shortcuts, roms[key]): continue

        new_roms[str(current_id)] = roms[key]
        new_roms[str(current_id)]["appid"] = app_id
        current_id += 1
        app_id -= 1

    return new_roms

def add_roms_to_shortcuts(roms):
    d = fetch_shortcuts()
    shortcuts = d["shortcuts"]
    shortcuts.update(roms)
    return d

def write_to_steam(roms):
    steam_id = get_steam_id()
    vdf.binary_dump(add_roms_to_shortcuts(roms),
                    open(f"{config["paths"]["steam_path"]}/userdata/{steam_id}/config/shortcuts.vdf", "wb"))
