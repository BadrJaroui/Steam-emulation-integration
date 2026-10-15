from utils.load_data import fetch_config
from steam.steam_helpers import get_steam_id, fetch_shortcuts
import vdf

config = fetch_config()

def add_games_to_vdf(shortcuts):
    vdf_file = fetch_shortcuts()

    current_id = len(vdf_file["shortcuts"])
    for shortcut in shortcuts.copy():
        vdf_file["shortcuts"][str(current_id)] = shortcuts[shortcut]
        current_id += 1

    vdf_file["shortcuts"].update(shortcuts)
    return vdf_file

def write_to_steam(shortcuts):
    steam_id = get_steam_id()
    vdf.binary_dump(add_games_to_vdf(shortcuts),
                    open(f"{config["paths"]["steam_path"]}/userdata/{steam_id}/config/shortcuts.vdf", "wb"))
