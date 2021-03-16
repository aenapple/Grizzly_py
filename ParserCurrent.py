import matplotlib.pyplot as plt


class EvseCurrent(object):
    def __init__(self):
        self.iac = []
        self.gfci = []
        self.seconds = []

    def get_iac(self):
        return self.iac

    def get_gfci(self):
        return self.gfci

    def get_seconds(self):
        return self.seconds

    def transform_data(self):
        file_input = open('LogFiles/LogEvse_CarCycle_1.txt', 'r')
        flag_first_line = True
        for line in file_input:
            str_record = line.replace(line[0:11], '')  # remove Date
            seconds_tmp = int(str_record[6:8]) + (int(str_record[3:5]) * 60) + (int(str_record[0:2]) * 3600)
            if flag_first_line:
                seconds_start = seconds_tmp
                flag_first_line = False
            # seconds_tmp = seconds_tmp - seconds_start
            self.seconds.append(seconds_tmp - seconds_start)

            str_record = line.replace(line[0:27], '')  # remove Date and Time
            for i in range(7):
                pos = str_record.find(',')
                if i == 3:
                    iac = int(str_record[0:pos])
                    self.iac.append(iac)
                if i == 4:
                    gfci = int(str_record[0:pos])
                    self.gfci.append(gfci)

                str_record = str_record.replace(str_record[0:pos + 1], '')

        # file_csv.write(str(seconds) + ',')
        # t_array.append(t)
        # file_csv.write(str(t) + ',' + '\n')
        # print(str_record)

        # file_csv.close()
        file_input.close()


if __name__ == '__main__':
    __doc__ = """
    ....
    """

    fig, ax = plt.subplots()

    evse_current = EvseCurrent()
    evse_current.transform_data()
    plt.ylim(0, 50000)
    ax.plot(evse_current.get_seconds(), evse_current.get_iac(), label="Iac")
    ax.plot(evse_current.get_seconds(), evse_current.get_gfci(), label="Gfci")

    ax.set(xlabel='time', ylabel='adc', title='Evse current')
    ax.grid()
    plt.legend()
    plt.show()

    print("OK")