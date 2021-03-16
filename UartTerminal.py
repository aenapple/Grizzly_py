import serial
import sys
import array as buf_array
# import time
# from LogFile import LogFile


class UartTerminal(object):
    def __init__(self):
        self.set_current = 0
        self.real_current = 0
        self.state = 0
        self.ComPort = None
        # self.set_current = 1128

    def get_set_current(self):
        return self.set_current

    def get_real_current(self):
        return self.real_current

    def get_state(self):
        return self.state

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

    def read_module(self, command, current):
        self.send_data(command, current)  # send command to module
        # time.sleep(0.1)
        read_data = self.ComPort.read(16)
        len_data = len(read_data)
        if len_data == 0:  #
            return 1, read_data  # 'No answer'

        self.state = read_data[0]
        self.set_current = read_data[1] + (read_data[2] << 8)
        # self.real_current = read_data[1] + (read_data[2] << 8)
        self.real_current = read_data[7] + (read_data[8] << 8)
        # print(read_data[6])
        # print(read_data[7])

        return 0, read_data  # 'OK'

    def send_data(self, command, current):
        # self.set_current = 1128
        # command = 0x00
        buffer = buf_array.array('B', [command])
        buffer.append(current & 0xFF)
        buffer.append(current >> 8)
        for i in range(12):
            buffer.append(0)

        crc = command
        for i in range(1, 14):
            crc = crc + buffer[i]
        crc = crc + 1
        buffer.append(crc)
        self.ComPort.write(buffer)  # send command to module

        # print(buffer)
        # print(len(buffer))

