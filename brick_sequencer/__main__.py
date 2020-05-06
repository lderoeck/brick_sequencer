import argparse
import csv
import os.path
from typing import *

import pandas as pd

from .BaseCaller import dropNonSequence
from .BaseGuesser import BaseGuesser
from .TimeCalculator import TimeCalculator
from . import colour
from .csvfile import CSVFile


def main():
    import sys

    parser = argparse.ArgumentParser(description="A base caller for the Lego brick sequencer")
    parser.add_argument("file", type=str, help="The file to process")
    parser.add_argument("-i", "--image-file", type=str, required=False, default=None,
                        help="Base name of the generated image files", metavar="IMAGE")

    args = parser.parse_args(sys.argv[1:])

    def processing(filename: str, column: str):
        df = pd.read_csv(args.file, index_col=False, usecols=["Time", column], na_values="-")
        df = df.dropna()  # Drop NaN values

        if args.image_file:
            from .image import export

            export(df[column], f"{args.image_file}_{column}.png")

        df = dropNonSequence(df)

        speed = TimeCalculator().calc_time(df[column].to_numpy())

        # Sequence the column and translate the results
        sequence = BaseGuesser.sequence(df, speed)

        print(speed)
        if args.image_file:
            import math
            from .image import export

            export(
                pd.concat(
                    # Convert the guessed colours to something we can export as image
                    [pd.Series([color] * math.floor(speed * 100), dtype="float32") for color in sequence["Colour"]]
                ),
                f"{args.image_file}_{column}_guess.png"
            )

        sequence = colour.translate(sequence)

        print(f"Sequence in column {column}:", "".join(sequence))

    CSVFile(args.file).process(processing)


if __name__ == "__main__":
    main()
