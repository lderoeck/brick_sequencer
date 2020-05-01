import math
from typing import *
import pandas as pd


def mean_square_error(confidence: pd.Series) -> float:
    """Calculates the MSE for a series of confidences"""
    return math.sqrt(((1 - confidence) ** 2).sum())


class BaseGuesser:
    def __init__(self):
        pass

    @classmethod
    def sequence(cls, data: pd.DataFrame,
                 speed: float,
                 max_offset: int = 10,
                 confidence_error: Callable[[pd.Series], float] = mean_square_error) -> pd.DataFrame:
        """
        Return a guessed sequence of bases (or colors in our case)

        Outputs something like the following:

                  Color  Confidence
        Section
        1         7      0.65
        2         1      0.57

        :param data: The (cleaned) data to determine the sequence off
        :param speed: The speed with which the sequence was read
        :param max_offset: The maximum amount of steps to offset the data to achieve better results
        :param confidence_error: Function to use when calculating the total confidence
        :return: A Pandas DataFrame with the section numbers as index and color and confidence as output
        """
        tries = dict()

        for offset in range(max_offset + 1):
            local_data = data.copy()
            local_data = local_data.iloc[offset:]

            # Guess the colours and confidences
            local_data = cls.guess(local_data, speed).reset_index(1)
            # Sort the colours by confidence in each section
            local_data = local_data.sort_values("Confidence", ascending=False).groupby("Section")
            # Get the most confident colour for each section and sort by section
            local_data = local_data.head(1).sort_values("Section")

            # Calculate the total confidence
            confidence = 1 - confidence_error(local_data["Confidence"])
            tries[offset] = (confidence, local_data)

        # Return the DataFrame for which we got the highest confidence
        return max(tries.items(), key=lambda x: x[1][0])[1][1]

    @classmethod
    def guess(cls, data: pd.DataFrame, speed: float) -> pd.DataFrame:
        """

        This function returns something like the following:

                          Confidence
        Section  Colour
        0        1        0.10
        0        2        0.09
        0        3        0.06
        0        4        0.05
        0        5        0.02
        0        6        0.03
        0        7        0.65
        1        0        0.01
        1        1        0.57
        ...      ...      ...

        Here (Section, Color) is a Pandas MultiIndex.  Colours without occurences do not appear in the index

        :param data: The (cleaned) data to guess the sequence of
        :param speed: The speed (in seconds per block) of the sequence read
        :return: A Pandas DataFrame with a confidence for each color in each section
        """

        # Determine the section/block count
        sections = int(math.ceil((data["Time"].max() - data["Time"].min()) / speed))

        # Ignore a warning from Pandas
        import warnings
        import pandas.core.common
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", pd.core.common.SettingWithCopyWarning)

            # Add a new Section column from the speed and timestamps
            data["Section"] = pd.cut(data["Time"],
                                     [speed * x + data["Time"].min() for x in range(sections + 1)],
                                     right=False).cat.codes

        # Make the Section and Time columns the index
        data = data.set_index(["Section", "Time"])

        # Clean up the column names
        data = pd.DataFrame(data[data.columns[0]].values, index=data.index, columns=["Colour"])

        confidences = data["Colour"].groupby("Section").value_counts(True)
        confidences = pd.DataFrame(confidences.values, columns=["Confidence"], index=confidences.index)

        return confidences


if __name__ == "__main__":
    import BaseCaller
    from brick_sequencer.TimeCalculator import *

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    column = "Colour_p4_03"
    file = "../trainingData/WWWWbbbbbbbbbbWWWW_speed5.csv"
    df = pd.read_csv(file, index_col=False, usecols=["Time", column])

    time = TimeCalculator().calc_time(df[column].to_numpy())

    print(time)

    print(BaseGuesser.sequence(BaseCaller.dropNonSequence(df), time))

    exit(0)
