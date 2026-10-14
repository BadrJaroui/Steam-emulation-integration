import vdf
import toml
from pathlib import Path

def fetch_config():
    with open('config.toml', 'r') as file:
        return toml.load(file)
config = fetch_config()

# convert entries to vdf
def read_users_file():
    users_file = f"{config["paths"]["steam_path"]}\\config\\loginusers.vdf"
    with open(users_file) as f:
        return vdf.load(f)

def get_shortcuts_file(): #C:\Program Files (x86)\Steam\
    steam_id = get_steam_id()
    return f"{config["paths"]["steam_path"]}\\userdata\\{steam_id}\\config\\shortcuts.vdf"

def get_steam_id():
    users = read_users_file()
    for item in users:
        for user_id in users[item]:
            if users[item][user_id]['AutoLogin'] == "1":
                return convert_steam64_to_steam3(int(user_id))
    
def convert_steam64_to_steam3(steam64):
    offset = 76561197960265728
    return steam64 - offset

def read_data():
    if not Path.exists(Path(f"{config["paths"]["steam_path"]}/userdata/{get_steam_id()}/config/shortcuts.vdf")):
        vdf.binary_dump({"shortcuts": {}}, open(f'{config["paths"]["steam_path"]}/userdata/{get_steam_id()}/config/shortcuts.vdf', 'wb'))
    with open(f"{config["paths"]["steam_path"]}/userdata/{get_steam_id()}/config/shortcuts.vdf", "rb") as f:
        data = vdf.binary_loads(f.read())
        if not any(data):
            data["shortcuts"] = {}
    return data

def add_games_to_vdf(shortcuts):
    vdf = read_data()
    vdf["shortcuts"].update(shortcuts)
    return vdf

def write_to_steam(shortcuts):
    vdf.binary_dump(add_games_to_vdf(shortcuts), open(f"{config["paths"]["steam_path"]}/userdata/{get_steam_id()}/config/shortcuts.vdf", "wb"))
