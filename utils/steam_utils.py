import utils.vdf_utils as vdf_utils

def get_shortcuts_file(steam_directory): #C:\Program Files (x86)\Steam\
    steam_id = get_steam_id(steam_directory)
    return f"{steam_directory}\\userdata\\{steam_id}\\config\\shortcuts.vdf"

def get_steam_id(steam_directory):
    users = vdf_utils.read_users_file(steam_directory)
    for item in users:
        for user_id in users[item]:
            if users[item][user_id]['MostRecent'] == "1":
                return convert_steam64_to_steam3(int(user_id))
    
def convert_steam64_to_steam3(steam64):
    offset = 76561197960265728
    return steam64 - offset