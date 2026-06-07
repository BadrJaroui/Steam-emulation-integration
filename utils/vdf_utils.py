import vdf
import os
from utils.utils import retrieve_directory_name, normalize_string
from utils.steam_utils import get_shortcuts_file

def read_data(file_path, steam_directory):
    if not os.path.exists(file_path):
        vdf.binary_dump({"shortcuts": {}}, open(f'{steam_directory}\\userdata\\410602222\\config\\shortcuts.vdf', 'wb'))
    with open(file_path, "rb") as f:
        data = vdf.binary_loads(f.read())
    return data

def read_users_file(steam_directory):
    users_file = f"{steam_directory}\\config\\loginusers.vdf"
    with open(users_file) as f:
        return vdf.load(f)

def remove_rom_entry_if_exists(name, system, steam_directory):
    data = read_data(get_shortcuts_file(steam_directory), steam_directory)
    for item in list(data):
        for game in list(data[item]):
            if name == data[item][game]['appname'] and system == normalize_string(
                retrieve_directory_name(data[item][game]['StartDir'])):
                print("game found")
                del data[item][game]
                vdf.binary_dump(data, open(f'{steam_directory}\\userdata\\410602222\\config\\shortcuts.vdf', 'wb'))

def get_last_shortcut(shortcuts_vdf):
    for item in shortcuts_vdf:
        if not shortcuts_vdf[item]:
            return None
        last_key = list(shortcuts_vdf[item].keys())[-1]
        return shortcuts_vdf[item][last_key]['appid']