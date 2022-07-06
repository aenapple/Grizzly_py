import time
import sys
from UartTerminal import UartTerminal
from LogFile import LogFile
import serial
import array as buf_array


IFC_EVSE_CMD_GET_STATE = 0x00
IFC_EVSE_CMD_START_SELFTEST = 0x01
IFC_EVSE_CMD_SET_STANDBY = 0x02
IFC_EVSE_CMD_ENABLE_CHARGING = 0x03
IFC_EVSE_CMD_DISABLE_CHARGING = 0x04
IFC_EVSE_CMD_UPDATE_CURRENT = 0x05
IFC_EVSE_CMD_SET_MAX_CURRENT = 0x06
IFC_EVSE_CMD_DISABLE = 0x07
IFC_EVSE_CMD_JUMP_TO_BOOT = 0x08
IFC_EVSE_CMD_RESET = 0x09
IFC_EVSE_CMD_GET_VERSION_1 = 0x0A
IFC_EVSE_CMD_GET_VERSION_2 = 0x0B
IFC_EVSE_CMD_GET_CRC_SIZE = 0x0C
IFC_EVSE_CMD_WIFI_CONNECTED = 0x0D
IFC_EVSE_CMD_WIFI_DISCONNECTED = 0x0E
IFC_EVSE_CMD_GET_SN_1 = 0x0F
IFC_EVSE_CMD_GET_SN_2 = 0x10
IFC_EVSE_CMD_GET_DATA_1 = 0x11
IFC_EVSE_CMD_GET_DATA_2 = 0x12
IFC_EVSE_CMD_GET_DATA_3 = 0x13

IFC_EVSE_STATE_SELFTEST = 0x00
IFC_EVSE_STATE_STANDBY = 0x01
IFC_EVSE_STATE_CAR_CONNECTED = 0x02
IFC_EVSE_STATE_CHARGING = 0x03
IFC_EVSE_STATE_CHARGING_COMPLETE = 0x04
IFC_EVSE_STATE_DISABLED = 0x05
IFC_EVSE_STATE_ERROR = 0x06
IFC_EVSE_STATE_NO_STATE = 0xFF


class Controller(object):
    def __init__(self):
        # self.set_current = 0
        self.evseState = IFC_EVSE_STATE_NO_STATE
        self.readData = 0
        self.result = 0
        self.uartTerminal = None

    def start(self, com_port, baud_rate):
        if self.uartTerminal is None:
            self.uartTerminal = UartTerminal()
            if self.uartTerminal.open(com_port, baud_rate) != 0:
                return 1

        while True:
            while True:
                self.result, self.readData = self.uartTerminal.read_module(IFC_EVSE_CMD_GET_STATE, 0)
                if self.result > 0:
                    # print("No answer")
                    time.sleep(1.0)
                    continue
                else:
                    break

            self.evseState = self.uartTerminal.get_state()
            if self.evseState != IFC_EVSE_STATE_DISABLED:
                self.uartTerminal.read_module(IFC_EVSE_CMD_DISABLE, 0)
                continue
            else:
                return 0

    def self_test(self):
        print("Started SELF_TEST")
        self.result, self.readData = self.uartTerminal.read_module(IFC_EVSE_CMD_START_SELFTEST, 0)
        if self.result > 0:
            return 1

        while True:
            self.result, self.readData = self.uartTerminal.read_module(IFC_EVSE_CMD_GET_STATE, 0)
            if self.result > 0:
                return 2

            self.evseState = self.uartTerminal.get_state()
            if self.evseState == IFC_EVSE_STATE_DISABLED:
                print("SelfTest - OK")
                return 0

            if self.evseState == IFC_EVSE_STATE_ERROR:
                print("SelfTest - ERROR")
                return 3

    def set_stanby(self):
        self.result, self.readData = self.uartTerminal.read_module(IFC_EVSE_CMD_SET_STANDBY, 0)  # set Standby
        if self.result > 0:
            return 1

        self.result, self.readData = self.uartTerminal.read_module(IFC_EVSE_CMD_ENABLE_CHARGING, 0)  # enable charging
        if self.result > 0:
            return 2

        return 0

    def start_log(self):
        log_file = LogFile()
        while True:
            time.sleep(9.7)

            self.result, self.readData = self.uartTerminal.read_module(IFC_EVSE_CMD_GET_DATA_1, 0)  # get Data1
            if self.result > 0:
                return 1
            log_file.write_record(self.readData)

            self.result, self.readData = self.uartTerminal.read_module(IFC_EVSE_CMD_GET_DATA_2, 0)  # get Data2
            if self.result > 0:
                return 1
            log_file.write_record(self.readData)

            self.result, self.readData = self.uartTerminal.read_module(IFC_EVSE_CMD_GET_DATA_3, 0)  # get Data3
            if self.result > 0:
                return 1

            log_file.write_record(self.readData)

            # return 0


if __name__ == '__main__':
    __doc__ = """
    ....
    """

    controller = Controller()

    while True:
        if controller.start('COM9', 115200) > 0:
            sys.exit(1)

        if controller.self_test() > 0:
            continue

        if controller.set_stanby() > 0:
            continue
        """ else:
            sys.exit(0) """

        if controller.start_log() > 0:
            continue

        sys.exit(0)


        """ evse_set_current = uartTerminal.get_set_current()
        evse_real_current = uartTerminal.get_real_current()
        # print(evse_state)
        # print(evse_set_current)
        print(evse_real_current)

        log_file = LogFile()
        log_file.write_record(read_data)

        if timer == 5:
            result, read_data = uartTerminal.read_module(EVSE_CMD_UPDATE_CURRENT, 1000)  # set current 10A
            if result > 0:
                print("No answer")
                sys.exit(5)
            else:
                print("Set 10A")

        if timer == 10:
            result, read_data = uartTerminal.read_module(EVSE_CMD_UPDATE_CURRENT, 2000)  # set current 20A
            if result > 0:
                print("No answer")
                sys.exit(5)
            else:
                print("Set 20A")
                timer = 0

        timer += 1 """

        """ if evse_state == IFC_EVSE_STATE_STANDBY:
            if cur_evse_state != evse_state:
                print("STANDBY")
                cur_evse_state = evse_state
            continue

        if evse_state == EVSE_STATE_CAR_CONNECTED:
            if cur_evse_state != evse_state:
                print("CAR_CONNECTED")
                cur_evse_state = evse_state
            continue

        if evse_state == EVSE_STATE_CHARGING:
            if cur_evse_state != evse_state:
                print("CHARGING")
                cur_evse_state = evse_state
            continue

        if evse_state == EVSE_STATE_CHARGING_COMPLETE:
            if cur_evse_state != evse_state:
                print("CHARGING COMPLETE")
                cur_evse_state = evse_state
            continue

        if evse_state == EVSE_STATE_DISABLED:
            if cur_evse_state != evse_state:
                print("DISABLED")
                cur_evse_state = evse_state
            continue

        # if evse_state == EVSE_STATE_ERROR
        if cur_evse_state != evse_state:
            print("ERROR")
            print(evse_error & 0xFF)
            cur_evse_state = evse_state

        # result, read_data = uartTerminal.read_module(EVSE_CMD_DISABLE, 0)
        # if result > 0:
        #    print("No answer")
        #    sys.exit(6) """

