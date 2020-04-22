import pandas as pd
import numpy as np
import re


class TimeCalculator:
    def __init__(self):
        pass

    def read_csv(self, input_file: str):
        df = pd.read_csv(input_file, sep=",")

        print(df["Colour_p4_01"].apply(lambda x: float(x) if re.match(r"\d", x) else 0))


if __name__ == "__main__":
    t = TimeCalculator()
    t.read_csv("../trainingData/WWWWbbbbbbbbbbWWWW_speed5.csv")
