from utils.load_data import fetch_config
from pathlib import Path
import vdf

config = fetch_config()

def fetch_shortcuts():
    steam_id = get_steam_id()
    if not Path.exists(Path(f"{config["paths"]["steam_path"]}/userdata/{steam_id}/config/shortcuts.vdf")):
        vdf.binary_dump({"shortcuts": {}},
                        open(f'{config["paths"]["steam_path"]}/userdata/{steam_id}/config/shortcuts.vdf', 'wb'))

    with open(f"{config["paths"]["steam_path"]}/userdata/{steam_id}/config/shortcuts.vdf", "rb") as f:
        data = vdf.binary_loads(f.read())
        if not any(data):
            data["shortcuts"] = {}
    return data

def fetch_users_file():
    users_file = f"{config["paths"]["steam_path"]}\\config\\loginusers.vdf"
    with open(users_file) as f:
        return vdf.load(f)

def get_steam_id():
    users = fetch_users_file()
    for item in users:
        for user_id in users[item]:
            if users[item][user_id]['AutoLogin'] == "1":
                return convert_steam64_to_steam3(int(user_id))
    
def convert_steam64_to_steam3(steam64):
    offset = 76561197960265728
    return steam64 - offset
