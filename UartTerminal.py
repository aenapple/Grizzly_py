import serial
import sys
import array as buf_array
# import time
# from LogFile import LogFile

COMMAND_GET_STATE = 0x00
COMMAND_START_CHARGING = 0x01
COMMAND_STOP_CHARGING = 0x02
COMMAND_CHANGE_CURRENT = 0x03


class UartTerminal(object):
    def __init__(self):
        self.index_print = 0
        self.ComPort = None
        self.set_current = 1128

    def open(self, com_port, baud_rate):
        # com_port = 'COM3'
        # baud_rate = 115200
        try:
            self.ComPort = serial.Serial(com_port, baud_rate, timeout=0.5)
        except serial.SerialException:
            print("Serial Exception:")
            print(sys.exc_info())
            return 1
        print(self.ComPort.out_waiting)
        print(self.ComPort.get_settings())
        print(self.ComPort.reset_output_buffer())
        return 0

    def read_module(self):
        self.send_data(0x03)  # send command to module
        # time.sleep(0.1)
        # read_line1 = self.ComPort.readline()
        read_data = self.ComPort.read(16)
        len_data = len(read_data)
        set_current = read_data[1] + (read_data[2] << 8)
        print(set_current)
        print(read_data[0])
        if len_data == 0:  #
            return 1, 'No main board'


        return 0, 'OK'

    def send_data(self, command):
        # self.set_current = 1128
        # command = 0x00
        buffer = buf_array.array('B', [command])
        buffer.append(self.set_current & 0xFF)
        buffer.append(self.set_current >> 8)
        for i in range(12):
            buffer.append(0)

        crc = command
        for i in range(1, 14):
            crc = crc + buffer[i]
        crc = crc + 1
        buffer.append(crc)
        self.ComPort.write(buffer)  # send command to module

        print(buffer)
        print(len(buffer))

