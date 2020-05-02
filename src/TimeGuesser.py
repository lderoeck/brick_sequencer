import re

import numpy as np
import pandas as pd


class TimeGuesser:
    def __init__(self):
        pass

    def split_sequence(self, array: list):
        white = np.vectorize(lambda x: x == "6.000" or x == 6)
        return self.clean_data(white(array))

    def _sanitise(self, symbol):
        if re.match("7", str(symbol)):
            return "Brown"
        if re.match("6", str(symbol)):
            return "White"
        if re.match("5", str(symbol)):
            return "Red"
        if re.match("4", str(symbol)):
            return "Yellow"
        if re.match("3", str(symbol)):
            return "Green"
        if re.match("2", str(symbol)):
            return "Blue"
        if re.match("1", str(symbol)):
            return "Black"
        return "None"

    def clean_data(self, array: list):
        """
        Creates most likely DNA string
        :param array:
        :return:
        """
        # Clean data to only contain colours
        full_sequence = []
        current = self._sanitise(array[0])
        length = 0

        for s in array:
            symbol = self._sanitise(s)
            if symbol == current:
                length += 1
                continue
            full_sequence.append({"symbol": current, "length": length})
            current = symbol
            length = 1

        full_sequence.append({"symbol": current, "length": length})

        # Filter out best guess for dna sequence
        sequence = []
        potential = []
        in_sequence = False

        for data in full_sequence:
            if not in_sequence:
                if data["symbol"] == "White":
                    in_sequence = True
                    potential.append(data)
                continue

            potential.append(data)

            if data["symbol"] == "White":
                sequence += potential
                potential = []
                continue

        # Filter out most likely wrong input
        # value = np.vectorize(lambda x: x["length"])
        # avg_length = np.average(value(sequence))
        # print(avg_length)
        # cleaned = []
        #
        # for data in sequence:
        #     amount = int(np.round(data["length"] / avg_length))
        #     if amount <= 0:
        #         continue
        #
        #     if len(cleaned) == 0 or cleaned[-1]["symbol"] != data["symbol"]:
        #         cleaned.append({"symbol": data["symbol"], "length": amount})
        #         continue
        #
        #     cleaned[-1]["length"] += amount

        return sequence


if __name__ == "__main__":
    guesser = TimeGuesser()

    column = "Colour_p4_01"
    file = "../trainingData/WWWWggggggggggggWWWW_speed5.csv"
    df = pd.read_csv(file, index_col=False, usecols=["Time", column])
    print(guesser.clean_data(df[column].to_numpy()))
