from utils.load_data import fetch_config
from steam.steam_helpers import fetch_shortcuts
import importer.scanner as scanner
import importer.mapper as mapper
import importer.writer as writer
import importer.import_images as images
from pathlib import Path

def script():
    config = fetch_config()

    for folder in Path.iterdir(Path(config["paths"]["roms_path"])):
        roms_data = scanner.scan_folder(folder)
        if roms_data is None:
            continue
        roms_shortcuts = mapper.create_shortcuts(roms_data)
        corrected_roms = writer.get_corrected_roms(roms_shortcuts)
        writer.write_to_steam(corrected_roms)

    d = fetch_shortcuts()
    shortcuts = d["shortcuts"]
    for key in shortcuts:
        images.import_images(shortcuts[key])
