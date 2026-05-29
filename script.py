import vdf
import os
import utils

emulators = {
    "gb": "D:\\Emulation\\Emulators\\RetroArch\\cores\\mgba_libretro.dll",
    "gba": "D:\\Emulation\\Emulators\\RetroArch\\cores\\mgba_libretro.dll",
    "gbc": "D:\\Emulation\\Emulators\\RetroArch\\cores\\mgba_libretro.dll",
    "rvz": {}, # gamecube
    "z64": "D:\\Emulation\\Emulators\\RetroArch\\cores\\mupen64plus_next_libretro.dll",
    "nds": "D:\\Emulation\\Emulators\\RetroArch\\cores\\melonds_libretro.dll",
    "nes": "D:\\Emulation\\Emulators\\RetroArch\\cores\\mesen_libretro.dll",
    "rvz": {}, # wii
    "m3u": "D:\\Emulation\\Emulators\\RetroArch\\cores\\swanstation_libretro.dll", # check if this actually works
    "iso": {}, # ps2, also supports other file types, look into that
    # "D:\\Emulation\\ROMs\\Sega Dreamcast": "D:\\Emulation\\Emulators\\RetroArch\\cores\\flycast_libretro.dll",
    # dreamcast, multi-disc games, figure that shit out
    "md": "D:\\Emulation\\Emulators\\RetroArch\\cores\\genesis_plus_gx_libretro.dll",
    "sfc": "D:\\Emulation\\Emulators\\RetroArch\\cores\\snes9x_libretro.dll"
}

def scrape_games():
    counter = 0
    appid_counter = -128908944
    d = {"shortcuts": {}}
    for root, dirs, files in os.walk("D:\\Emulation\\ROMs"):
        for file in files:
            if not file.split(".")[1] in emulators.keys():
                continue

            d["shortcuts"].update(utils.generateEntry(
                entryid=str(counter),
                appid=appid_counter - 1,
                name=file.split("(")[0].strip(),
                target= fetch_target(root, file),
                startdir=root
            ))

            counter += 1
            appid_counter -= 1
    return d

def fetch_target(root, file):
    file_extension = file.split(".")[1]
    if file_extension in emulators.keys() and file_extension == "rvz":
        return f'"D:\\Emulation\\Emulators\\Dolphin\\Dolphin.exe" "{root}\\{file}" "/f"'
    # if file_extension in emulators.keys() and file_extension == "iso":
    #     pass

    # default to retroarch
    if file_extension in emulators.keys():
        return f'"D:\\Emulation\\Emulators\\RetroArch\\retroarch.exe" -L "{emulators.get(file.split(".")[1])}" "{root}\\{file}"'


def write_to_steam():
    new_shortcuts = scrape_games()
    print(new_shortcuts)
    vdf.binary_dump(new_shortcuts, open('C:\\Program Files (x86)\\Steam\\userdata\\410602222\\config\\shortcuts.vdf', 'wb'))

write_to_steam()