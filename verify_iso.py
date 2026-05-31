import pycdlib

def check_iso_system(file_path):
    magic_offset_gc = 0x1c
    magic_bytes_gc = b'\xc23\x9f'

    magic_offset_wii = 0x18
    magic_bytes_wii = b']\x1c\x9e'

    if check_magic_bytes(file_path, magic_offset_gc, magic_bytes_gc):
        return "gamecube"
    if check_magic_bytes(file_path, magic_offset_wii, magic_bytes_wii):
        return "wii"
    
    check_sony_result = check_sony_system(file_path)
    if check_sony_system is not None:
        return check_sony_result

    return None

def check_magic_bytes(file_path, offset, magic_bytes):
    with open(file_path, "rb") as f:
        f.seek(offset)
        magic = f.read(3)
    if magic == magic_bytes:
        return True

    return False

def check_sony_system(file_path):
    iso = pycdlib.PyCdlib()
    file = iso.open(file_path)
    for roots, dirs, files in iso.walk(iso_path="/"):
        for file in files:
            # To be changed: check contents of system.cnf
            if "system.cnf" in file.lower():
                return "ps2"
            # check for psp
    
    return None