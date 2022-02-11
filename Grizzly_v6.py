import time
import sys
from UartTerminal_v6 import UartTerminal
import array as buf_array
import serial

UcipCmd_GetState = 0x00
UcipCmd_StartSelfTest = 1  # 0x01
UcipCmd_SetStandby = 2  # 0x02
UcipCmd_EnableCharging = 3  # 0x03
UcipCmd_DisableCharging = 4  # 0x04
UcipCmd_UpdateCurrent = 0x05
UcipCmd_SetMaxCurrent = 0x06
UcipCmd_SetDisabled = 0x07
UcipCmd_JumpToBoot = 0x08
UcipCmd_Reset = 0x09
UcipCmd_GetVersion = 0x0A
UcipCmd_GetCrc32 = 0x0B
UcipCmd_SetState = 0x0C
UcipCmd_SendVersion = 0x0D
UcipCmd_SendSerialNumber = 0x0E
UcipCmd_GetSerialNumber = 0x0F
UcipCmd_GetPartitionTable = 0x10
UcipCmd_GetCommand = 0x11
UcipCmd_StartUploadUpdateFile = 0x12
UcipCmd_GetMaxSizePacket = 0x13
UcipCmd_SendMaxSizePacket = 0x14

UcipState_NoState = 0x00
UcipState_SelfTest = 0x01
UcipState_Standby = 0x02
UcipState_CarConnected = 0x03
UcipState_CarCharging = 0x04
UcipState_ChargingComplete = 0x05
UcipState_Disabled = 0x06
UcipState_Error = 0x07
UcipState_PowerUp = 0x08
# UcipState_ReadyUpdateFile = 0x09
# UcipState_TransferringUpdateFile = 0x0A,
UcipState_ServerNotConnected = 0x0B		# WiFi module state
UcipState_ServerConnected = 0x0C		# WiFi module state




if __name__ == '__main__':
    __doc__ = """
    ....
    """
    # print(buffer)
    # print(len(buffer))
    # sys.exit(0)

    uartTerminal = UartTerminal()
    if uartTerminal.open('COM7', 115200) != 0:
        sys.exit(1)

    # creat data buffer
    data_buffer = buf_array.array('B')
    for i in range(uartTerminal.get_size_data()):
        data_buffer.append(0)

    # waiting start charger
    while True:
        result, read_data = uartTerminal.read_module()
        if result > 0:
            if result == 2:
                print("CRC Error")
            continue

        print(read_data)
        uartTerminal.send_module(UcipCmd_GetCommand, data_buffer)
        continue

        rx_command = uartTerminal.get_command()
        if rx_command == UcipCmd_GetCommand:
            uartTerminal.send_module(UcipCmd_GetMaxSizePacket, data_buffer)
            continue

        if rx_command == UcipCmd_SendMaxSizePacket:
            rx_data = uartTerminal.get_rx_data()
            uartTerminal.send_module(UcipCmd_SendMaxSizePacket, data_buffer)
            print("Max packet size:")
            print(rx_data[0])
            break

    # str_file_input = "GS06-0008.ufs"
    # file_input = open(str_file_input, 'rb')

    result, read_data = uartTerminal.read_module()
    if result > 0:
        # file_input.close()
        sys.exit(2)

    rx_command = uartTerminal.get_command()
    if rx_command == UcipCmd_GetCommand:
        uartTerminal.send_module(UcipCmd_StartUploadUpdateFile, data_buffer)

    # while True:
    sys.exit(10)
