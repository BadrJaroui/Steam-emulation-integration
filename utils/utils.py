def generateEntry(entryid, appid, name, target, startdir):
    format = {
            entryid: {
                "appid": appid,
                "appname": name,
                "exe": (
                    target
                ),
                "StartDir": f'{startdir}',
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

    return format

def parse_game_name(file_name):
    if "(" in file_name:
        return file_name.split("(")[0].strip()
    if "[" in file_name:
        return file_name.split("[")[0].strip()
    if "." in file_name:
        return file_name.split(".")[0].strip()
    
def normalize_string(x):
    return x.replace(" ", "")\
            .replace("-", "")\
            .replace("_", "")\
            .lower()

def retrieve_directory_name(file_path):
    if "\\" in file_path:
        return file_path.lower().split("\\roms")[1].split("\\")[1]
    if "/" in file_path:
        return file_path.lower().split("/roms")[1].split("/")[1]

    return ValueError(f"Invalid path: {file_path}")

def toUnsigned(n):
    return n & 0xFFFFFFFF