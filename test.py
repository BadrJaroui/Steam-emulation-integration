magic_offset = 0x18
magic_bytes = b']\x1c\x9e'

with open("D:\\Emulation\\ROMs\\Nintendo Wii\\New Super Mario Bros. Wii.iso", "rb") as f:
    f.seek(magic_offset)
    magic = f.read(3)

if magic == magic_bytes:
    print("Wii")

f.close()