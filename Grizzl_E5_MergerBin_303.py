import time
import sys
import os
import binascii

BINFILE_APPLICATION_ADDRESS = 0xA000


if __name__ == '__main__':
    __doc__ = """
    ....
    """
    # print(buffer)
    # print(len(buffer))
    # sys.exit(0)
    args = sys.argv[1:]
    str_file_bootloader = args[0]
    str_file_application = args[1]

    str_file_output = str_file_application + "_flash"
    file_output = open(str_file_output, 'wb')
    file_input = open(str_file_bootloader, 'rb')
    file_size = os.stat(str_file_bootloader)
    number_bytes = file_size.st_size

    file_read = file_input.read(number_bytes)
    file_output.write(file_read)
    file_input.close()
    if number_bytes < BINFILE_APPLICATION_ADDRESS:
        for k in range(BINFILE_APPLICATION_ADDRESS - number_bytes):
            file_output.write(bytes([255]))

    file_input = open(str_file_application, 'rb')
    file_size = os.stat(str_file_application)
    number_bytes = file_size.st_size
    file_read = file_input.read(number_bytes)
    file_output.write(file_read)

    file_output.close()
    file_input.close()



