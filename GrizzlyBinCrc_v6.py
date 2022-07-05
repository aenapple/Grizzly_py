import time
import sys
import os
import binascii

BINFILE_OFFSET = 0x300
BINFILE_SIZE_OFFSET = 0x4
BINFILE_VERSION_OFFSET = 0x10
BINFILE_VERSION_SIZE = 0x10
BINFILE_NAME_FILE = "Grizzl_E6_app.bin"


if __name__ == '__main__':
    __doc__ = """
    ....
    """
    data = None
    #  name_file = os.getcwd() + '\\' + BINFILE_NAME_FILE
    with open(BINFILE_NAME_FILE, 'rb') as file:
        data = bytearray(file.read())
    filesize = len(data)  # + 4  # +CRC
    print(hex(filesize))
    # data[BINFILE_OFFSET+BINFILE_SIZE_OFFSET] = (filesize >> 24) & 0xFF
    # data[BINFILE_OFFSET+BINFILE_SIZE_OFFSET + 1] = (filesize >> 16) & 0xFF
    # data[BINFILE_OFFSET+BINFILE_SIZE_OFFSET + 2] = (filesize >> 8) & 0xFF
    # data[BINFILE_OFFSET+BINFILE_SIZE_OFFSET + 3] = filesize & 0xFF
    data = data[: -4]
    crc = binascii.crc32(data)
    print(hex(crc))
    data = data + crc.to_bytes(4, 'little')
    
    filename = data[BINFILE_OFFSET+BINFILE_VERSION_OFFSET: BINFILE_OFFSET+BINFILE_VERSION_OFFSET+BINFILE_VERSION_SIZE]
    filename = filename[:filename.find(0)]
    if filename.find(0x20) > -1:
        filename = filename[:filename.find(0x20)]
    filename = filename.decode()+'.bin'
    with open(filename, 'wb') as file:
        file.write(data)
    print(filename)
