from steam.steam_helpers import get_steam_id, fetch_shortcuts
from utils.load_data import fetch_config
import vdf

config = fetch_config()

def add_roms_to_shortcuts(roms):
    d = fetch_shortcuts()
    shortcuts = d["shortcuts"]
    current_id = len(shortcuts)

    for key in roms.copy():
        roms[str(current_id)] = roms[key]
        current_id += 1

    shortcuts.update(roms)
    return d

def write_to_steam(shortcuts):
    steam_id = get_steam_id()
    vdf.binary_dump(add_roms_to_shortcuts(shortcuts),
                    open(f"{config["paths"]["steam_path"]}/userdata/{steam_id}/config/shortcuts.vdf", "wb"))
