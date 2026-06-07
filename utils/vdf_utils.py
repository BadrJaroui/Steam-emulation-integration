import vdf
import os
from utils.utils import retrieve_directory_name, normalize_string
from utils.steam_utils import get_shortcuts_file

def read_data(file_path):
    if not os.path.exists(file_path):
        vdf.binary_dump({"shortcuts": {}}, open('C:\\Program Files (x86)\\Steam\\userdata\\410602222\\config\\shortcuts.vdf', 'wb'))
    with open(file_path, "rb") as f:
        data = vdf.binary_loads(f.read())
    return data

def read_users_file(steam_directory):
    users_file = f"{steam_directory}\\config\\loginusers.vdf"
    with open(users_file) as f:
        return vdf.load(f)

def remove_rom_entry_if_exists(name, system):
    data = read_data(get_shortcuts_file('C:\\Program Files (x86)\\Steam'))
    for item in list(data):
        for game in list(data[item]):
            if name == data[item][game]['appname'] and system == normalize_string(
                retrieve_directory_name(data[item][game]['StartDir'])):
                print("game found")
                del data[item][game]
                vdf.binary_dump(data, open('C:\\Program Files (x86)\\Steam\\userdata\\410602222\\config\\shortcuts.vdf', 'wb'))