import matplotlib.pyplot as plt

EVSE_DATA_DATA1_CODE = 17
EVSE_DATA_DATA2_CODE = 18
EVSE_DATA_DATA3_CODE = 19


class EvseData(object):
    def __init__(self):
        self.seconds = []
        # Data 1:
        self.tRelay = []
        self.pilot = []
        self.diode = []
        self.line1_DetectGnd = []
        self.line2_DetectGnd = []
        self.line1_WeldRelay = []
        self.line2_WeldRelay = []
        # Data 2:
        self.tEvse = []
        self.currentAdc = []
        self.gfciAdc = []
        self.tCpu = []
        self.vRef = []
        self.current_mA = []
        self.voltage_mV = []
        # Data 3:
        self.gfciBase = []
        self.currentBase = []
        self.gfciLow = []
        self.gfciHigh = []
        self.reserved1 = []
        self.reserved2 = []
        self.reserved3 = []

    def get_seconds(self):
        return self.seconds

    def get_t_relay(self):  # ADC - 12bits
        return self.tRelay

    def get_pilot(self):  # ADC - 12bits
        return self.pilot

    def get_diode(self):  # ADC - 12bits
        return self.diode

    def get_line1_detect_gnd(self):  # ADC - 12bits
        return self.line1_DetectGnd

    def get_line2_detect_gnd(self):  # ADC - 12bits
        return self.line2_DetectGnd

    def get_line1_weld_relay(self):  # ADC - 12bits
        return self.line1_WeldRelay

    def get_line2_weld_relay(self):  # ADC - 12bits
        return self.line2_WeldRelay

    def get_t_evse(self):  # ADC - 12bits
        return self.tEvse

    def get_current_adc(self):  # ADC - 12bits
        return self.currentAdc

    def get_gfci_adc(self):  # ADC - 12bits
        return self.gfciAdc

    def get_t_cpu(self):  # ADC - 12bits
        return self.tCpu

    def get_v_ref(self):  # ADC - 12bits
        return self.vRef

    def get_current_ma(self):  # 80000 max
        return self.current_mA

    def get_voltage_mv(self):  # 300000 max
        return self.voltage_mV

    def get_gfci_base(self):  # ADC - 12bits
        return self.gfciBase

    def get_current_base(self):  # ADC - 12bits
        return self.currentBase

    def get_gfci_low(self):  # - ???
        return self.gfciLow

    def get_gfci_high(self):  # - ???
        return self.gfciHigh


    def transform_data(self):
        t_array = []
        s_array = []

        file_input = open('LogFiles\LogEvse-0715-16.42.txt', 'r')
        # file_csv = open('LogTemperature_' + hex(number_module).replace('0x', '') + '.csv', 'w')
        flag_first_line = True
        for line in file_input:
            # file_csv.write(line[0:10] + ',')
            str_record_sec = line.replace(line[0:11], '')  # remove Date
            seconds_tmp = int(str_record_sec[6:8]) + (int(str_record_sec[3:5]) * 60) + (int(str_record_sec[0:2]) * 3600)
            if flag_first_line:
                seconds_start = seconds_tmp
                flag_first_line = False
            # self.seconds.append(seconds_tmp - seconds_start)

            str_record = line.replace(line[0:27], '')  # remove Date and Time
            pos_data_code = str_record.find(',')
            data_code = int(str_record[0:pos_data_code])
            str_record = str_record.replace(str_record[0:pos_data_code + 1], '', 1)

            if data_code == EVSE_DATA_DATA1_CODE:
                k = 0
                self.seconds.append(seconds_tmp - seconds_start)
            elif data_code == EVSE_DATA_DATA2_CODE:
                k = 1
            else:
                k = 2

            # print(str_record)
            for i in range(7):
                pos = str_record.find(',')
                if i == 0:  # 1st record
                    if k == 0:
                        t_relay = int(str_record[0:pos])
                        self.tRelay.append(t_relay)
                    elif k == 1:
                        t_evse = int(str_record[0:pos])
                        self.tEvse.append(t_evse)
                    else:
                        gfci_base = int(str_record[0:pos])
                        self.gfciBase.append(gfci_base)
                if i == 1:  # 2nd record
                    if k == 0:
                        pilot = int(str_record[0:pos])
                        self.pilot.append(pilot)
                    elif k == 1:
                        current_adc = int(str_record[0:pos])
                        self.currentAdc.append(current_adc)
                    else:
                        current_base = int(str_record[0:pos])
                        self.currentBase.append(current_base)
                if i == 2:  # 3rd record
                    if k == 0:
                        diode = int(str_record[0:pos])
                        self.diode.append(diode)
                    elif k == 1:
                        gfci_adc = int(str_record[0:pos])
                        self.gfciAdc.append(gfci_adc)
                    else:
                        gfci_low = int(str_record[0:pos])
                        self.gfciLow.append(gfci_low)
                if i == 3:  # 4th record
                    if k == 0:
                        line1_detect_gnd = int(str_record[0:pos])
                        self.line1_DetectGnd.append(line1_detect_gnd)
                    elif k == 1:
                        t_cpu = int(str_record[0:pos])
                        self.tCpu.append(t_cpu)
                    else:
                        gfci_high = int(str_record[0:pos]) * 1000
                        self.gfciHigh.append(gfci_high)
                if i == 4:  # 5th record
                    if k == 0:
                        line2_detect_gnd = int(str_record[0:pos])
                        self.line2_DetectGnd.append(line2_detect_gnd)
                    elif k == 1:
                        v_ref = int(str_record[0:pos])
                        self.vRef.append(v_ref)
                    else:
                        # reserved1 = int(str_record[0:pos])
                        self.gfciHigh.append(0)
                if i == 5:  # 6th record
                    if k == 0:
                        line1_weld_relay = int(str_record[0:pos])
                        self.line1_WeldRelay.append(line1_weld_relay)
                    elif k == 1:
                        current_ma = int(str_record[0:pos]) * 10
                        self.current_mA.append(current_ma)
                    else:
                        # reserved2 = int(str_record[0:pos])
                        self.gfciHigh.append(0)
                if i == 6:
                    if k == 0:
                        line2_weld_relay = int(str_record[0:pos])
                        self.line2_WeldRelay.append(line2_weld_relay)
                    elif k == 1:
                        voltage_mv = int(str_record[0:pos]) * 10
                        self.voltage_mV.append(voltage_mv)
                    else:
                        # reserved3 = int(str_record[0:pos])
                        self.gfciHigh.append(0)

                str_record = str_record.replace(str_record[0:pos + 1], '', 1)

        # file_csv.write(str(seconds) + ',')
        # t_array.append(t)
        # file_csv.write(str(t) + ',' + '\n')
        # print(str_record)

        # file_csv.close()
        file_input.close()


"""def transform_data(file_name):
    t_array = []
    s_array = []
    file_input = open(file_name, 'r')
    file_csv = open(file_name.replace('txt', 'csv'), 'w')
    for line in file_input:
        if (line.find('2020') < 0) or (line.find('ERR') >= 0) or (line.find('OK') >= 0):  # empty or error line
            continue

        file_csv.write(line[0:10] + ',')
        str_record = line.replace(line[0:11], '')  # remove Date

        seconds = int(str_record[6:8]) + (int(str_record[3:5]) * 60) + (int(str_record[0:2]) * 3600)
        s_array.append(seconds)
        file_csv.write(str(seconds) + ',')

        t = (int(str_record[16:20]) + int(str_record[21:25]) + int(str_record[26:30])) / 300
        t_array.append(t)
        file_csv.write(str(t) + ',' + '\n')
        print(str_record, end='')

    file_csv.close()
    file_input.close()
    return t_array, s_array"""


if __name__ == '__main__':
    __doc__ = """
    ....
    """

    fig, axes = plt.subplots(3, 1)

    evse_data = EvseData()
    evse_data.transform_data()
    plt.ylim(0, 5000)
    # ax[0].set_xlim(0, 5000)
    axes[0].plot(evse_data.get_seconds(), evse_data.get_t_relay(), label="TRelay")
    axes[0].plot(evse_data.get_seconds(), evse_data.get_t_evse(), label="TEvse")
    axes[0].plot(evse_data.get_seconds(), evse_data.get_t_cpu(), label="TCpu")
    axes[0].plot(evse_data.get_seconds(), evse_data.get_v_ref(), label="Vref")

    axes[1].plot(evse_data.get_seconds(), evse_data.get_pilot(), label="Pilot")
    axes[1].plot(evse_data.get_seconds(), evse_data.get_diode(), label= "Diode")
    # axes[1].plot(evse_data.get_seconds(), evse_data.get_line1_detect_gnd(), label="GND-L1")
    axes[1].plot(evse_data.get_seconds(), evse_data.get_line2_detect_gnd(), label="GND-L2")
    axes[1].plot(evse_data.get_seconds(), evse_data.get_line1_weld_relay(), label="Weld-L1")
    # axes[1].plot(evse_data.get_seconds(), evse_data.get_line2_weld_relay(), label="Weld-L2")

    axes[2].plot(evse_data.get_seconds(), evse_data.get_current_adc(), label="IAC-ADC")
    axes[2].plot(evse_data.get_seconds(), evse_data.get_gfci_adc(), label="GFCI-ADC")
    axes[2].plot(evse_data.get_seconds(), evse_data.get_gfci_base(), label="GFCI-base")
    axes[2].plot(evse_data.get_seconds(), evse_data.get_current_base(), label="IAC-base")


    axes[0].set(xlabel='time', ylabel='adc', title='Evse state', ylim=(0, 4200))
    axes[0].grid(True)
    axes[0].legend(loc='upper left')
    axes[1].set(xlabel='time', ylabel='adc')
    axes[1].grid(True)
    axes[1].legend(loc='upper left')
    axes[2].set(xlabel='time', ylabel='adc')
    axes[2].grid(True)
    axes[2].legend(loc='upper left')
    # plt.legend()
    plt.show()

    print("OK")