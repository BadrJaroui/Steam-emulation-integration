import vdf

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

def readData():
    with open("C:/Program Files (x86)/Steam/userdata/410602222/config/shortcuts.vdf", "rb") as f:
        data = vdf.binary_loads(f.read())
    print(data)
    
def toUnsigned(n):
    return n & 0xFFFFFFFF