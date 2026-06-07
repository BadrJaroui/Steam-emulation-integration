import vdf
import os
import time

import utils.vdf_utils as vdf_utils
import utils.utils as utils
import utils.steam_utils as steam_utils
from import_assets.import_images import import_images

# TODO: make it so that multidisc games generate m3u file if not exists
# TODO: give user the option for multidisc to import 1 multidisc, all multidiscs or create an m3u file

# TODO: user should be able to manually select what consoles/emulators they wish to use
# TODO: create a ui for the application

# TODO: improve image selection: some games have similar names and receive the same images

def retrieve_paths():
    while True:
        ROMS_PATH = input("Enter Rom folder path: ")
        if not os.path.isdir(ROMS_PATH):
            print("Not a valid path.")
            continue
        break

    while True:
        EMULATORS_PATH = input("Enter Emulators folder path: ")
        if not os.path.isdir(EMULATORS_PATH):
            print("Not a valid path.")
            continue
        break

    while True:
        STEAM_PATH = input("Enter Steam folder path")
        if not os.path.isdir(EMULATORS_PATH):
            print("Not a valid path.")
            continue
        break

    return (ROMS_PATH, EMULATORS_PATH, STEAM_PATH)

# ROMS_PATH, EMULATORS_PATH = retrieve_paths()
ROMS_PATH = "D:\\Emulation\\ROMs"
EMULATORS_PATH = "D:\\Emulation\\Emulators"
STEAM_PATH = "C:\\Program Files (x86)\\Steam"

# for string matching, remove spaces and use lowercase
folder_names = {
    "nes": ["nes", "nintendo entertainment system", "famicom", "nintendo family computer", "hyundai comboy", "comboy"],
    "snes": ["snes", "super nintendo entertainment system", "super nes", 
             "super nintendo", "sfc", "super famicom", "super fc", "hyundai super comboy", "hyundai sc", "super comboy"],
    "n64": ["n64", "nintendo 64", "hyundai comboy 64", "comboy 64"],
    "gc": ["nintendo gamecube", "gamecube", "gc", "gcn", "ngc"],
    "wii": ["nintendo wii", "wii"],
    "gb": ["gb", "nintendo gameboy", "gameboy", "ngb"],
    "gbc": ["gbc", "nintendo gameboy color", "gameboy color", "ngbc"],
    "gba": ["gba", "nintendo gameboy advance", "gameboy advance", "ngba"],
    "nds": ["nds", "nintendo ds", "ds", "ndsi", "nintendo dsi", "dsi", "nds lite", "nintendo ds lite", "ds lite"],
    "genesis": ["sega genesis", "genesis", "sega mega drive", "mega drive", "sega md", "md"],
    "dreamcast": ["dreamcast", "sega dreamcast", "sega dc", "dc"],
    "ps1": ["ps1", "playstation", "sony playstation", "sony playstation 1", "sony ps1", "sony ps", "sony psx", "psx", "ps one", "ps"],
    "ps2": ["ps2", "sony playstation 2", "sony ps2", "ps two", "playstation 2"],
    "xbox": ["xbox", "microsoft xbox", "ms xbox", "original xbox", "og xbox", "xbox classic"],
}

associated_cores = {
    "gb": f"{EMULATORS_PATH}\\RetroArch\\cores\\mgba_libretro.dll",
    "gba": f"{EMULATORS_PATH}\\RetroArch\\cores\\mgba_libretro.dll",
    "gbc": f"{EMULATORS_PATH}\\RetroArch\\cores\\mgba_libretro.dll",
    "n64": f"{EMULATORS_PATH}\\RetroArch\\cores\\mupen64plus_next_libretro.dll",
    "nds": f"{EMULATORS_PATH}\\RetroArch\\cores\\melonds_libretro.dll",
    "nes": f"{EMULATORS_PATH}\\RetroArch\\cores\\mesen_libretro.dll",
    "ps1": f"{EMULATORS_PATH}\\RetroArch\\cores\\swanstation_libretro.dll",
    "genesis": f"{EMULATORS_PATH}\\RetroArch\\cores\\genesis_plus_gx_libretro.dll",
    "snes": f"{EMULATORS_PATH}\\RetroArch\\cores\\snes9x_libretro.dll",
    "wii": "",
    "gc": "",
    "ps2": "",
    "dreamcast": "",
}

def scrape_games():
    d = vdf_utils.read_data(steam_utils.get_shortcuts_file(STEAM_PATH), STEAM_PATH)

    counter = 0
    appid_counter = vdf_utils.get_last_shortcut(d)
    if appid_counter is None:
        appid_counter = -128908944

    for root, dirs, files in os.walk(f"{ROMS_PATH}"):
        for file in files:
            system = check_folder_name(root)
            if system == None:
                continue
            if system == "ps1" or system == "dreamcast":
                if not verify_multidisc_game(file, system):
                    continue

            vdf_utils.remove_rom_entry_if_exists(file.split(".")[0], system, STEAM_PATH)

            d["shortcuts"].update(utils.generateEntry(
                entryid=str(counter),
                appid=appid_counter - 1,
                name=utils.parse_game_name(file),
                target= fetch_target(system, f"{root}\\{file}"),
                startdir=root
            ))
            counter += 1
            appid_counter -= 1

            # try:
            #     import_images(STEAM_PATH, appid_counter, utils.parse_game_name(file))
            # except Exception as e:
            #     continue
    return d

def check_folder_name(file_path: str):
    for names in folder_names:
        for name in folder_names[names]:
            normalized_name = utils.normalize_string(name)
            directory_to_check = utils.retrieve_directory_name(file_path)
            normalized_directory = utils.normalize_string(directory_to_check)

            if normalized_name == normalized_directory:
                return names
 
    return None

def fetch_target(system, file_path):
    emulator = associated_cores.get(system)
    if emulator != None:
        if system == "ps2":
            return f'"{EMULATORS_PATH}\\PCSX2\\pcsx2-qt.exe" "{file_path}" -nogui -fullscreen'
        if system == "wii" or system == "gc":
            return f'"{EMULATORS_PATH}\\Dolphin\\Dolphin.exe" "{file_path}" "/f"'
        if system == "dreamcast":
            return "fart"
        return f'"{EMULATORS_PATH}\\RetroArch\\retroarch.exe" -L "{emulator}" "{file_path}"'

def verify_multidisc_game(file, system):
    if system == "ps1" or system == "dreamcast":
        file_extension = file.split(".")[1]
        if file_extension == "m3u":
            return True
        return False

    return False

def write_to_steam():
    start = time.time()
    new_shortcuts = scrape_games()
    vdf.binary_dump(new_shortcuts, open(f'{STEAM_PATH}\\userdata\\410602222\\config\\shortcuts.vdf', 'wb'))
    print(new_shortcuts)
    print("Games exported to Steam")
    end = time.time()
    print(f"Time taken to run the code was {end-start} seconds")

write_to_steam()