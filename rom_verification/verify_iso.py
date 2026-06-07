import pycdlib

# TODO: check for psp, xbox, xbox 360, maybe ps3

GC_MAGIC_OFFSET = 0x1c
GC_MAGIC_BYTES = b'\xc23\x9f'
GC_BYTES_TO_CHECK = 3

WII_MAGIC_OFFSET = 0x18
WII_MAGIC_BYTES = b']\x1c\x9e'
WII_BYTES_TO_CHECK = 3

XBOX_MAGIC_OFFSET = 0x10000
XBOX_MAGIC_BYTES = b'MICROSOFT*XBOX*MEDIA'
XBOX_BYTES_TO_CHECK = 20

def check_iso_system(file_path):
    if check_magic_bytes(file_path, GC_MAGIC_OFFSET, GC_MAGIC_BYTES, GC_BYTES_TO_CHECK):
        return "gamecube"
    if check_magic_bytes(file_path, WII_MAGIC_OFFSET, WII_MAGIC_BYTES, WII_BYTES_TO_CHECK):
        return "wii"
    if check_magic_bytes(file_path, XBOX_MAGIC_OFFSET, XBOX_MAGIC_BYTES, XBOX_BYTES_TO_CHECK):
        return "xbox"
    
    check_sony_result = check_sony_system(file_path)
    if check_sony_system is not None:
        return check_sony_result

    return None

def check_magic_bytes(file_path, offset, magic_bytes, bytes_to_read):
    with open(file_path, "rb") as f:
        f.seek(offset)
        magic = f.read(bytes_to_read)
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