import serial
import sys
import array as buf_array
# import time
# from LogFile import LogFile

UART_SIZE_PACKET = 24

UCIP_TITLE_SIZE = 2   # 2 bytes - 'G' + 'R'
UCIP_PACKET_SIZE = 2  # 2 bytes - size packet in bytes
UCIP_CMD_SIZE = 1     # 1 byte - command/status
UCIP_CRC_SIZE = 1     # 1 byte
UCIP_DATA_SIZE = (UART_SIZE_PACKET - UCIP_TITLE_SIZE - UCIP_PACKET_SIZE - UCIP_CMD_SIZE - UCIP_CRC_SIZE)  # 18 bytes


UCIP_INDEX_TITLE = 0
UCIP_INDEX_PACKET_SIZE = (UCIP_INDEX_TITLE + UCIP_TITLE_SIZE)
UCIP_INDEX_CMD = (UCIP_INDEX_PACKET_SIZE + UCIP_PACKET_SIZE)
UCIP_INDEX_DATA = (UCIP_INDEX_CMD + UCIP_CMD_SIZE)
UCIP_INDEX_STATE = UCIP_INDEX_DATA
UCIP_INDEX_ERROR = UCIP_INDEX_DATA


class UartTerminal(object):
    def __init__(self):
        self.set_current = 0
        self.real_current = 0
        self.command = 0
        self.state = 0
        self.error = 0
        self.ComPort = None
        self.rx_data = buf_array.array('B')
        self.tx_data = buf_array.array('B')
        for i in range(UCIP_DATA_SIZE):
            self.rx_data.append(0)
        for i in range(UCIP_DATA_SIZE):
            self.tx_data.append(0)
        # self.set_current = 1128

    def get_set_current(self):
        return self.set_current

    def get_real_current(self):
        return self.real_current

    def get_command(self):
        return self.command

    def get_state(self):
        return self.state

    def get_error(self):
        return self.error

    def get_size_data(self):
        return UCIP_DATA_SIZE

    def get_rx_data(self):
        return self.rx_data

    def get_tx_data(self):
        return self.tx_data

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
        read_data = self.ComPort.read(UART_SIZE_PACKET)
        len_data = len(read_data)
        if len_data == 0:  #
            return 1, read_data  # 'No answer'

        crc = self.calc_crc(read_data, UART_SIZE_PACKET - 1)
        if crc != read_data[UART_SIZE_PACKET - 1]:
            return 2, read_data  # 'CRC Error'

        self.command = read_data[UCIP_INDEX_CMD]
        self.state = read_data[UCIP_INDEX_CMD]
        self.error = read_data[UCIP_INDEX_DATA]
        for i in range(UCIP_DATA_SIZE):
            self.rx_data[i] = read_data[i + UCIP_INDEX_DATA]

        return 0, read_data  # 'OK'

    def send_module(self, command, data):
        # self.set_current = 1128
        # command = 0x00
        buffer = buf_array.array('B', [0x47, 0x52]) # 'G', 'R'
        buffer.append(UART_SIZE_PACKET & 0xFF)
        buffer.append(0)
        buffer.append(command)
        for i in range(UCIP_DATA_SIZE):
            buffer.append(data[i])

        crc = self.calc_crc(buffer, UART_SIZE_PACKET - 1)
        buffer.append(crc)
        self.ComPort.write(buffer)  # send command to module

    def calc_crc(self, buf_data, size_data):
        crc = 0
        for i in range(0, size_data):
            crc = crc + buf_data[i]
        crc = crc + 1
        crc = crc & 0xFF
        return crc


        # print(buffer)
        # print(len(buffer))

