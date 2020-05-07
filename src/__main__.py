import argparse
import math

import pandas as pd

from .BaseCaller import dropNonSequence
from .BaseGuesser import BaseGuesser
from .TimeCalculator import TimeCalculator
from . import colour
from .colour import Colour
from .csvfile import CSVFile


def block(speed: float):
    state = False
    while True:
        state = not state
        if state:
            yield [Colour.BLACK.value] * math.floor(speed * 100)
        else:
            yield [Colour.WHITE.value] * math.floor(speed * 100)


def main():
    import sys

    parser = argparse.ArgumentParser(description="A base caller for the Lego brick sequencer")
    parser.add_argument("file", type=str, help="The file to process")
    parser.add_argument("-i", "--image", type=str, required=False, default=None,
                        help="Base name of the generated image files", metavar="IMAGE")
    parser.add_argument("--height", type=int, required=False, default=16,
                        help="Height of each sequence in the output image", metavar="HEIGHT")

    args = parser.parse_args(sys.argv[1:])

    def processing(filename: str, column: str):
        df = pd.read_csv(args.file, index_col=False, usecols=["Time", column], na_values="-")
        df = df.dropna()  # Drop NaN values

        if args.image:
            from .image import export

            export(df[column], f"{args.image}_{column}_raw.png", args.height)

        df = dropNonSequence(df)

        speed = TimeCalculator().calc_time(df[column].to_numpy())

        # Sequence the column and translate the results
        sequence = BaseGuesser.sequence(df, speed)

        if args.image:
            import math
            from .image import export_multiple

            tmp = block(speed)
            speed_sequence = pd.concat([pd.Series(next(tmp), dtype="float32") for _ in range(sequence["Colour"].size)])

            guess_sequence = pd.concat(
                # Convert the guessed colours to something we can export as image
                [pd.Series([color] * math.floor(speed * 100), dtype="float32") for color in sequence["Colour"]]
            )

            export_multiple([df[column], speed_sequence, guess_sequence], f"{args.image}_{column}.png", args.height)

        sequence = colour.translate(sequence)

        print(f"Sequence in column {column}:", "".join(sequence))

    CSVFile(args.file).process(processing)


if __name__ == "__main__":
    main()
