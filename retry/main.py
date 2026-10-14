import core.scanner as scanner
import core.mapper as mapper
import core.writer as writer
from pathlib import Path

def main():
    config = scanner.fetch_config()
    for folder in Path.iterdir(Path(config["paths"]["roms_path"])):
        roms_data = scanner.scan_folder(folder)
        if roms_data is None:
            continue
        roms_shortcuts = mapper.create_shortcuts(roms_data)
        writer.write_to_steam(roms_shortcuts)

if __name__ == "__main__":
    main()