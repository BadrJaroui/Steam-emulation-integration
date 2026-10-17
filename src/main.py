from utils.load_data import fetch_config
import importer.scanner as scanner
import importer.mapper as mapper
import importer.writer as writer
import importer.import_images as images
from pathlib import Path

def main():
    config = fetch_config()

    for folder in Path.iterdir(Path(config["paths"]["roms_path"])):
        roms_data = scanner.scan_folder(folder)
        if roms_data is None:
            continue
        roms_shortcuts = mapper.create_shortcuts(roms_data)
        writer.write_to_steam(roms_shortcuts)

        for rom in roms_shortcuts:
            print(roms_shortcuts[rom])
            images.import_images(roms_shortcuts[rom])

if __name__ == "__main__":
    main()
