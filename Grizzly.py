import time
import sys
from UartTerminal import UartTerminal
import array as buf_array

if __name__ == '__main__':
    __doc__ = """
    ....
    """


    # print(buffer)
    # print(len(buffer))
    # sys.exit(0)

    uartTerminal = UartTerminal()
    if uartTerminal.open('COM4', 115200) != 0:
        sys.exit(2)

    while True:

        uartTerminal.read_module()
        time.sleep(2.0)
