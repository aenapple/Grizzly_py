

class TSensor:
    def __init__(self):
        self.size_table = 34
        self.table = [
            [43, -40],
            [60, -35],
            [84, -30],
            [115, -25],
            [156, -20],
            [209, -15],
            [276, -10],
            [359, -5],
            [461, 0],
            [584, 5],
            [728, 10],
            [893, 15],
            [1078, 20],
            [1280, 25],
            [1493, 30],
            [1714, 35],
            [1937, 40],
            [2156, 45],
            [2367, 50],
            [2566, 55],
            [2751, 60],
            [2919, 65],
            [3070, 70],
            [3205, 75],
            [3323, 80],
            [3427, 85],
            [3518, 90],
            [3597, 95],
            [3664, 100],
            [3722, 105],
            [3771, 110],
            [3813, 115],
            [3849, 120],
            [3880, 125]
        ]

    def get_temperature(self, adc_value):
        if adc_value <= self.table[0][0]:
            return self.table[0][1]

        if adc_value >= self.table[self.size_table - 1][0]:
            return self.table[self.size_table - 1][1]

        for i in range(1, self.size_table):
            if adc_value < self.table[i][0]:
                adc_range = self.table[i][0] - self.table[i - 1][0]
                index_table = i - 1
                break

        steps = 0
        for i in range(5):
            steps += adc_range / 5
            if adc_value < (self.table[index_table][0] + steps):
                return self.table[index_table][1] + i

        return self.table[index_table+1][1]
