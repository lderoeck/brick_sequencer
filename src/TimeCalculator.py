import pandas as pd
import numpy as np
import re


class TimeCalculator:
    def __init__(self):
        self.white = np.vectorize(lambda x: x == "6.000" or x == 6)

    def calc_time(self, sequence, num_white=8, time_step=0.01):
        """
        Calculates time needed to read a single base
        :param sequence: array (row) of sequence data
        :param num_white: amount of white bases present in sequence (start/end)
        :param time_step: amount of time passed each step (default 10ms)
        :return:
        """
        data = self.white(sequence)
        return np.floor(np.sum(data) / num_white) * time_step

    def read_csv(self, input_file: str):
        df = pd.read_csv(input_file, sep=",")

        arrays = df.transpose().to_numpy()

        for i in range(len(arrays) - 1):
            print(self.calc_time(arrays[i]))


if __name__ == "__main__":
    t = TimeCalculator()
    t.read_csv("../trainingData/WWWWbbbbbbbbbbWWWW_speed5.csv")
    t.read_csv("../trainingData/WWWWggggggggggggWWWW_speed5.csv")
