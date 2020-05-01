import argparse
import csv
import os.path
from typing import *

import pandas as pd

from .BaseCaller import dropNonSequence
from .BaseGuesser import BaseGuesser
from .TimeCalculator import TimeCalculator
import src.colour as colour


def main(args):
    parser = argparse.ArgumentParser(description="A base caller for the Lego brick sequencer")
    parser.add_argument("file", type=str, help="The file to process")
    parser.add_argument("-i", "--image-file", type=str, required=False, default=None,
                        help="Location of the image file to generate", metavar="IMAGE")

    args = parser.parse_args(args)


    # Check file exists
    if not os.path.exists(args.file):
        raise ValueError("Filename does not exist")

    # Get the file header
    with open(args.file, encoding="utf-8-sig") as f:
        header: List[str] = next(csv.reader(f))

    # Check the Time column
    if "Time" not in header:
        raise ValueError("Time column missing from data file")

    # Filter the Time column
    header.remove("Time")

    # Repeat for each column in the file
    for column in header:
        df = pd.read_csv(args.file, index_col=False, usecols=["Time", column], na_values="-")
        df = df.dropna()  # Drop NaN values

        if args.image_file:
            from .image import export

            export(df[column], f"{args.image_file}_{column}.png")

        df = dropNonSequence(df)

        speed = TimeCalculator().calc_time(df[column].to_numpy())

        # Sequence the column and translate the results
        sequence = BaseGuesser.sequence(df, speed)
        sequence = colour.translate(sequence)

        print(f"Sequence in column {column}:", "".join(sequence))


if __name__ == "__main__":
    import sys
    main(sys.argv)
