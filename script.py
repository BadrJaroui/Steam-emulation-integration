import vdf
import os
import utils

# TODO: figure out how to handle subdirectories inside console roms folders
# TODO: check by file type for proper dll rather than path

emulators = {
    "D:\\Emulation\\ROMs\\GameBoy": "D:\\Emulation\\Emulators\\RetroArch\\cores\\mgba_libretro.dll",
    "D:\\Emulation\\ROMs\\GameBoy Advance": "D:\\Emulation\\Emulators\\RetroArch\\cores\\mgba_libretro.dll",
    "D:\\Emulation\\ROMs\\GameBoy Color": "D:\\Emulation\\Emulators\\RetroArch\\cores\\mgba_libretro.dll",
    "D:\\Emulation\\ROMs\\GameCube": {},
    "D:\\Emulation\\ROMs\\Nintendo 64": "D:\\Emulation\\Emulators\\RetroArch\\cores\\mupen64plus_next_libretro.dll",
    "D:\\Emulation\\ROMs\\Nintendo DS": "D:\\Emulation\\Emulators\\RetroArch\\cores\\melonds_libretro.dll",
    "D:\\Emulation\\ROMs\\Nintendo Entertainment System": "D:\\Emulation\\Emulators\\RetroArch\\cores\\mesen_libretro.dll",
    "D:\\Emulation\\ROMs\\Nintendo Wii": {},
    "D:\\Emulation\\ROMs\\PlayStation": "D:\\Emulation\\Emulators\\RetroArch\\cores\\swanstation_libretro.dll",
    "D:\\Emulation\\ROMs\\PS2": {},
    "D:\\Emulation\\ROMs\\Sega Dreamcast": "D:\\Emulation\\Emulators\\RetroArch\\cores\\flycast_libretro.dll",
    "D:\\Emulation\\ROMs\\Sega Genesis": "D:\\Emulation\\Emulators\\RetroArch\\cores\\genesis_plus_gx_libretro.dll",
    "D:\\Emulation\\ROMs\\Super Nintendo Entertainment System": "D:\\Emulation\\Emulators\\RetroArch\\cores\\snes9x_libretro.dll"
}

def scrape_games():
    counter = 0
    appid_counter = -128908944
    d = {"shortcuts": {}}
    for root, dirs, files in os.walk("D:\\Emulation\\ROMs"):
        dll = emulators.get(root)
        if root == "D:\\Emulation\\ROMs\\PS2" or root == "D:\\Emulation\\ROMs\\Nintendo Wii" or root == "D:\\Emulation\\ROMs\\GameCube" or root == "D:\\Emulation\\ROMs\\GameBoy Advance" or root == "D:\\Emulation\\ROMs\\PlayStation" or root == "D:\\Emulation\\ROMs\\GameBoy Advance\\Romhacks":
            continue
        for file in files:
            d["shortcuts"].update(utils.generateEntry(
                entryid=str(counter),
                appid=appid_counter - 1,
                name=file.split("(")[0].strip(),
                target= '"D:\\Emulation\\Emulators\\RetroArch\\retroarch.exe" '
                        f'-L "{dll}" '
                        f'"{root}\\{file}"',
                startdir=root
            ))
            counter += 1
            appid_counter -= 1
    return d

def write_to_steam():
    new_shortcuts = scrape_games()
    print(new_shortcuts)
    vdf.binary_dump(new_shortcuts, open('C:\\Program Files (x86)\\Steam\\userdata\\410602222\\config\\shortcuts.vdf', 'wb'))

write_to_steam()