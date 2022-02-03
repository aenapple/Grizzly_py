import time
import sys
from UartTerminal_v6 import UartTerminal
import serial

UcipCmd_GetState = 0x00
UcipCmd_StartSelfTest = 0x01
UcipCmd_SetStandby = 0x02
UcipCmd_EnableCharging = 0x03
UcipCmd_DisableCharging = 0x04
UcipCmd_UpdateCurrent = 0x05
UcipCmd_SetMaxCurrent = 0x06
UcipCmd_SetDisabled = 0x07
UcipCmd_JumpToBoot = 0x08
UcipCmd_Reset = 0x09
UcipCmd_GetVersion = 0x0A
UcipCmd_GetCrc32 = 0x0B
UcipCmd_SetState = 0x0C
UcipCmd_SetVersion = 0x0D
UcipCmd_SetSerialNumber = 0x0E
UcipCmd_GetSerialNumber = 0x0F
UcipCmd_GetPartitionTable = 0x10
UcipCmd_GetCommand = 0x11

UcipState_NoState = 0x00
UcipState_SelfTest = 0x01
UcipState_Standby = 0x02
UcipState_CarConnected = 0x03
UcipState_CarCharging = 0x04
UcipState_ChargingComplete = 0x05
UcipState_Disabled = 0x06
UcipState_Error = 0x07
UcipState_PowerUp = 0x08


if __name__ == '__main__':
    __doc__ = """
    ....
    """
    # print(buffer)
    # print(len(buffer))
    # sys.exit(0)

    uartTerminal = UartTerminal()
    if uartTerminal.open('COM3', 115200) != 0:
        sys.exit(1)

    while True:
        result, read_data = uartTerminal.read_module()
        if result > 0:
            if result == 2:
                print("CRC Error")
            # print("No answer")
            continue
        else:
            print(read_data)

        uartTerminal.send_module(UcipCmd_SetStandby, read_data)
