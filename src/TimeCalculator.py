import pandas as pd
import numpy as np
import re


class TimeCalculator:
    def __init__(self):
        pass

    def read_csv(self, input_file: str):
        df = pd.read_csv(input_file, sep=",")

        arrays = df.transpose().to_numpy()

        vf = np.vectorize(lambda x: x == "6.000" or x == 6)

        for i in range(len(arrays)-1):
            array = arrays[i]
            simpl = vf(array)
            # print(simpl)
            print(sum(simpl)/8)

        # print(arrays)

        # for i in range(len(arrays)-1):
        #     array = arrays[i]
        #     for j in range(len(array)-1):

        # keys = df.keys()
        # for i in range(1, len(keys)):
        #     key = keys[i]
        #     print(df.get(key).apply(lambda x: float(str(x)) if re.match(r"\d", str(x)) else 0))

        # print(df.apply(lambda x: float(x) if re.match(r"\d", x) else 0))


if __name__ == "__main__":
    t = TimeCalculator()
    t.read_csv("../trainingData/WWWWbbbbbbbbbbWWWW_speed5.csv")
    t.read_csv("../trainingData/WWWWggggggggggggWWWW_speed5.csv")
