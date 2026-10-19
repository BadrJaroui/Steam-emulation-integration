from script import script

def main():
    script()

if __name__ == "__main__":
    main()

# TODO: fix playlists folder creation in every roms directory
# TODO: non-retroarch emulators support
# TODO: multidisc support
# TODO: add emulators & launch commands manually
# TODO: add folders for scanning manually
# TODO: remove hardcoded emulator/retroarch paths in emulators.json
# TODO: loop through folders recursively

# TODO: CLI:
# - Allow user to manually select a folder for scanning
# - Allow user to manually add emulators, containing path to emulator, launch commands and extensions to scan
# --console flag for only importing a specific console's roms
# --art-only flag for only importing art