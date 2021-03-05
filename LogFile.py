import time
import datetime
from datetime import date


class LogFile(object):
    # def __init__(self):
    #    self.str_temp = "None"

    # def __open(self):
    #    pass

    def write_record(self, record):
        datetime_object = datetime.datetime.now()
        print(datetime_object)
        today = datetime_object.strftime("%m/%d/%Y-%H:%M:%S.%f-")

        try:
            full_record = today
            # str_temp = record[1] + (record[2] << 8)
            # full_record = full_record + str_temp
            for i in range(7):
                str_temp = str(record[i*2+1] + (record[i*2+2] << 8))
                full_record = full_record + str_temp + ","

            full_record = full_record + "\n"
            # str_temp = record.decode()
            # full_record = today + record.replace('temp from '.encode(), '')
            # full_record = today + str_temp
            print(full_record)
        except:
            print("ERROR record")
            return

        file_out = open('LogEvse.txt', 'a')
        file_out.write(full_record)
        file_out.close()

