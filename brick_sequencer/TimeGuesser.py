import re

import numpy as np
import pandas as pd


def theoretical_speed(speed: float):
    """
    Extrapolated speed function from data provided, won't give accurate read results but can be used as a starting point
    for determining a more accurate speed.
    :param speed: Speed setting used in the reader
    :return: Rough estimation for amount of blocks/base, needs to be fine-tuned for the actual data input
    """
    return 250 / speed


class TimeGuesser:
    def __init__(self):
        pass

    def _sanitise(self, symbol):
        """
        Cleans data to correct colour values
        :param symbol: Input symbol
        :return: Correct colour value
        """
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
        Clean data to only contain colours
        :param array: Raw input stream of reader
        :return: List of cleaned data with lengths
        """
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

        return full_sequence

    def split_sequence(self, array: list):
        """
        Remove input before and after sequence
        :param array: Raw input stream of reader
        :return: List of cleaned sequence data with lengths
        """
        sequence = []
        potential = []
        in_sequence = False

        full_sequence = self.clean_data(array)

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

        return sequence

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


if __name__ == "__main__":
    guesser = TimeGuesser()

    column = "Colour_p4_01"
    file = "../trainingData/WWWWyggbgrbrbygyrbrrWWWW_speed30.csv"
    df = pd.read_csv(file, index_col=False, usecols=["Time", column])
    print(guesser.split_sequence(df[column].to_numpy()))
