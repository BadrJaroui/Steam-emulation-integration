from steam.steam_helpers import fetch_shortcuts
from utils.load_data import fetch_config
import importer.scanner as scanner
import importer.mapper as mapper
import importer.writer as writer
import importer.import_images as images
import importer.multidisc as multidisc
from pathlib import Path

def script():
    config = fetch_config()

    for folder in Path(config["paths"]["roms_path"]).rglob('*'):
        print(f"Looking through {folder}...")
        # Create m3u playlists for multidisc games if applicable
        emulator = scanner.get_emulator_from_folder_name(folder)
        multidisc_roms = None
        if not emulator is None and emulator[1]["multi_disc"] is True:
            multidisc_roms = multidisc.create_playlists(folder, emulator)

        # Fetches roms
        roms_data = scanner.scan_folder(folder, roms_to_ignore=multidisc_roms)
        if roms_data is None:
            continue

        # Puts roms in valid format for Steam
        roms_shortcuts = mapper.create_shortcuts(roms_data)

        # Assigns proper IDs to roms and writes them to Steam
        corrected_roms = writer.get_corrected_roms(roms_shortcuts)
        writer.write_to_steam(corrected_roms)

    # Checks for (missing) artwork and imports images
    d = fetch_shortcuts()
    shortcuts = d["shortcuts"]
    for key in shortcuts:
        print(f"Fetching artwork for {shortcuts[key]["appname"]}...")
        images.import_images(shortcuts[key])
