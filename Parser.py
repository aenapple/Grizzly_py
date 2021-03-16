import matplotlib.pyplot as plt


class EvseData(object):
    def __init__(self):
        self.ac1_gnd = []
        self.ac2_gnd = []
        self.ac_relay = []
        self.iac = []
        self.gfci = []
        self.pilot = []
        self.diode = []
        self.seconds = []

    def get_ac1_gnd(self):
        return self.ac1_gnd

    def get_ac2_gnd(self):
        return self.ac2_gnd

    def get_ac_relay(self):
        return self.ac_relay

    def get_iac(self):
        return self.iac

    def get_gfci(self):
        return self.gfci

    def get_pilot(self):
        return self.pilot

    def get_diode(self):
        return self.diode

    def get_seconds(self):
        return self.seconds

    def transform_data(self):
        t_array = []
        s_array = []

        file_input = open('LogFiles/LogEvse_CarCycle_1.txt', 'r')
        # file_csv = open('LogTemperature_' + hex(number_module).replace('0x', '') + '.csv', 'w')
        flag_first_line = True
        for line in file_input:
            # file_csv.write(line[0:10] + ',')
            str_record_sec = line.replace(line[0:11], '')  # remove Date
            seconds_tmp = int(str_record_sec[6:8]) + (int(str_record_sec[3:5]) * 60) + (int(str_record_sec[0:2]) * 3600)
            if flag_first_line:
                seconds_start = seconds_tmp
                flag_first_line = False
            self.seconds.append(seconds_tmp - seconds_start)

            str_record = line.replace(line[0:27], '')  # remove Date and Time
            # print(str_record)
            for i in range(7):
                pos = str_record.find(',')
                if i == 0:
                    ac1_gnd = int(str_record[0:pos])
                    self.ac1_gnd.append(ac1_gnd)
                if i == 1:
                    ac2_gnd = int(str_record[0:pos])
                    self.ac2_gnd.append(ac2_gnd)
                if i == 2:
                    ac_relay = int(str_record[0:pos])
                    self.ac_relay.append(ac_relay)
                if i == 3:
                    iac = int(str_record[0:pos])
                    self.iac.append(iac)
                if i == 4:
                    gfci = int(str_record[0:pos])
                    self.gfci.append(gfci)
                if i == 5:
                    pilot = int(str_record[0:pos])
                    self.pilot.append(pilot)
                if i == 6:
                    diode = int(str_record[0:pos])
                    self.diode.append(diode)

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

    fig, ax = plt.subplots()

    str_label = [
        "Ac1_gnd"
        "Ac2_gnd",
        "AcRelay",
        "Iac",
        "Gfci",
        "Pilot",
        "Diode",
    ]

    evse_data = EvseData()
    evse_data.transform_data()
    plt.ylim(0, 5000)
    ax.plot(evse_data.get_seconds(), evse_data.get_ac1_gnd(), label="Ac1_gnd")
    ax.plot(evse_data.get_seconds(), evse_data.get_ac2_gnd(), label="Ac2_gnd")
    ax.plot(evse_data.get_seconds(), evse_data.get_ac_relay(), label= "AcRelay")
    ax.plot(evse_data.get_seconds(), evse_data.get_iac(), label="Iac")
    ax.plot(evse_data.get_seconds(), evse_data.get_gfci(), label="Gfci")
    ax.plot(evse_data.get_seconds(), evse_data.get_pilot(), label="Pilot")
    ax.plot(evse_data.get_seconds(), evse_data.get_diode(), label="Diode")

    ax.set(xlabel='time', ylabel='adc', title='Evse state')
    ax.grid()
    plt.legend()
    plt.show()

    print("OK")

