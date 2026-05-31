import vdf
import os
import utils
import pycdlib
import pyisotools

# TODO: support for all pcsx2 compatible file extensions
# TODO: figure out what to do with multi-disc games
# TODO: paths as user input, one for emulator locations, one for retroarch cores locations, one for roms
# TODO: refactor fetch_core
# TODO: find a way to identify game's system that's more reliable than checking folder/file extension
# TODO: check for m3u files: if exists, ignore cue files in folder. if not, use cue file

file_extensions = [
    "gb",
    "gba",
    "gbc",
    "z64",
    "nds",
    "nes",
    "m3u",
    "cue",
    "md",
    "sfc"
]

def fetch_core(file_extension, root):
    if file_extension == "m3u" or file_extension == "cue":
        if "dreamcast" in root.lower():
            return "D:\\Emulation\\Emulators\\RetroArch\\cores\\flycast_libretro.dll"
        if "playstation" in root.lower():
            return "D:\\Emulation\\Emulators\\RetroArch\\cores\\swanstation_libretro.dll"

    if file_extension == "gb":
        return "D:\\Emulation\\Emulators\\RetroArch\\cores\\mgba_libretro.dll"
    if file_extension == "gba":
        return "D:\\Emulation\\Emulators\\RetroArch\\cores\\mgba_libretro.dll"
    if file_extension == "gbc":
        return "D:\\Emulation\\Emulators\\RetroArch\\cores\\mgba_libretro.dll"
    if file_extension == "z64":
        return "D:\\Emulation\\Emulators\\RetroArch\\cores\\mupen64plus_next_libretro.dll"
    if file_extension == "nds":
        return "D:\\Emulation\\Emulators\\RetroArch\\cores\\melonds_libretro.dll"
    if file_extension == "nes":
        return "D:\\Emulation\\Emulators\\RetroArch\\cores\\mesen_libretro.dll"
    if file_extension == "md":
        return "D:\\Emulation\\Emulators\\RetroArch\\cores\\genesis_plus_gx_libretro.dll"
    if file_extension == "sfc":
        return "D:\\Emulation\\Emulators\\RetroArch\\cores\\snes9x_libretro.dll"

def scrape_games():
    counter = 0
    appid_counter = -128908944
    d = {"shortcuts": {}}
    for root, dirs, files in os.walk("D:\\Emulation\\ROMs"):
        for file in files:
            if not file.split(".")[1] in file_extensions:
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
    if file_extension in file_extensions and file_extension == "rvz":
        return f'"D:\\Emulation\\Emulators\\Dolphin\\Dolphin.exe" "{root}\\{file}" "/f"'
    if file_extension in file_extensions and file_extension == "iso":
        return f'"D:\Emulation\Emulators\PCSX2\pcsx2-qt.exe" "{root}\\{file}" -nogui -fullscreen'
    if file_extension in file_extensions:
        return f'"D:\\Emulation\\Emulators\\RetroArch\\retroarch.exe" -L "{fetch_core(file.split(".")[1], root)}" "{root}\\{file}"'


def write_to_steam():
    new_shortcuts = scrape_games()
    print(new_shortcuts)
    vdf.binary_dump(new_shortcuts, open('C:\\Program Files (x86)\\Steam\\userdata\\410602222\\config\\shortcuts.vdf', 'wb'))

write_to_steam()