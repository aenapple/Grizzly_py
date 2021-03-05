import time
import sys
from UartTerminal import UartTerminal
from LogFile import LogFile


EVSE_CMD_GET_STATE = 0x00
EVSE_CMD_START_SELFTEST = 0x01
EVSE_CMD_SET_STANDBY = 0x02
EVSE_CMD_UPDATE_CURRENT = 0x03
EVSE_CMD_DISABLE = 0x04

EVSE_STATE_SELFTEST = 0x00
IFC_EVSE_STATE_STANDBY = 0x01
EVSE_STATE_CAR_CONNECTED = 0x02
EVSE_STATE_CHARGING = 0x03
EVSE_STATE_CHARGING_COMPLETE = 0x04
EVSE_STATE_DISABLED = 0x05
EVSE_STATE_ERROR = 0x06


if __name__ == '__main__':
    __doc__ = """
    ....
    """
    # print(buffer)
    # print(len(buffer))
    # sys.exit(0)

    uartTerminal = UartTerminal()
    if uartTerminal.open('COM4', 115200) != 0:
        sys.exit(1)

    time.sleep(0.2)
    result, read_data = uartTerminal.read_module(EVSE_CMD_GET_STATE, 0)
    if result > 0:
        print("No answer")
        sys.exit(2)

    evse_state = uartTerminal.get_state()
    if evse_state != EVSE_STATE_DISABLED:
        result, read_data = uartTerminal.read_module(EVSE_CMD_DISABLE, 0)
        if result > 0:
            print("No answer")
            sys.exit(3)

        time.sleep(0.2)
        result, read_data = uartTerminal.read_module(EVSE_CMD_GET_STATE, 0)
        if result > 0:
            print("No answer")
            sys.exit(3)

        evse_state = uartTerminal.get_state()
        if evse_state != EVSE_STATE_DISABLED:
            print("START - Error")
            sys.exit(3)

    print("Started SELF_TEST")
    result, read_data = uartTerminal.read_module(EVSE_CMD_START_SELFTEST, 0)
    if result > 0:
        print("No answer")
        sys.exit(4)
    while True:
        result, read_data = uartTerminal.read_module(EVSE_CMD_GET_STATE, 0)
        if result > 0:
            print("No answer")
            sys.exit(4)

        evse_state = uartTerminal.get_state()
        if evse_state == EVSE_STATE_DISABLED:
            break

        if evse_state == EVSE_STATE_ERROR:
            print("SELF_TEST - Error")
            sys.exit(4)

        time.sleep(0.1)

    print("SELF_TEST - OK")
    result, read_data = uartTerminal.read_module(EVSE_CMD_SET_STANDBY, 20)  # Standby, current 20A
    if result > 0:
        print("No answer")
        sys.exit(5)

    cur_evse_state = EVSE_STATE_DISABLED
    while True:
        time.sleep(1.0)
        result, read_data = uartTerminal.read_module(EVSE_CMD_GET_STATE, 0)
        if result > 0:
            print("No answer")
            sys.exit(6)

        evse_state = uartTerminal.get_state()
        evse_set_current = uartTerminal.get_set_current()
        evse_real_current = uartTerminal.get_real_current()
        print(evse_state)
        # print(evse_set_current)
        # print(evse_real_current)

        log_file = LogFile()
        log_file.write_record(read_data)

        if evse_state == IFC_EVSE_STATE_STANDBY:
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
            print("ERRO")
            cur_evse_state = evse_state

        result, read_data = uartTerminal.read_module(EVSE_CMD_DISABLE, 0)
        if result > 0:
            print("No answer")
            sys.exit(6)
