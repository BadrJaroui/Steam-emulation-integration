from pathlib import Path

def format_rom(rom_path):
    return Path(rom_path).stem.split(" (")[0]

def get_roms(folder):
    return [str(f) for f in Path(folder).glob('**/*') if f.is_file()]

def get_playlist_names(folder):
    playlists = []
    files = get_roms(folder)
    for file in files:
        if file.suffix == ".m3u":
            playlists.append(format_rom(file))
    return playlists

def get_multidisc_roms(folder, emulator):
    titles = {}
    roms = get_roms(folder)
    if roms is None:
        return
    for rom in roms:
        if "disc" in rom.lower() and Path(rom).suffix in emulator[1]["extensions"]:
            if not format_rom(rom) in titles:
                titles[format_rom(rom)] = [rom]
                continue
            else:
                titles[format_rom(rom)].append(rom)
    return titles

def get_first_discs(folder, emulator):
    first_discs = []
    roms = get_multidisc_roms(folder, emulator)
    for key in roms:
        first_discs.append(roms[key])
    return first_discs

def create_playlists(folder, emulator):
    roms = get_multidisc_roms(folder, emulator)
    if roms is None or emulator[0] == "ps2":
        return None
    playlists_dir = Path(f"{folder}/Playlists")
    if not playlists_dir.exists():
        Path.mkdir(f"{folder}/Playlists")

    for key in roms:
        playlist_path = Path(f"{playlists_dir}/{key}.m3u")
        contents = ""
        for disc in roms[key]:
            contents += str(disc)
            contents += "\n"
        with open(playlist_path, "w") as f:
            f.write(contents)
    return roms
