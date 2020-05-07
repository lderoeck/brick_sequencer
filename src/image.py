from typing import *
import pandas as pd
from PIL import Image

from .colour import colour_rgb


def export(series: pd.Series, filename: str, height: int = 16) -> bool:
    image = Image.new("RGB", (series.size, height))

    image_data = []
    for _ in range(height):
        image_data.extend(series.tolist())

    image_data = [x for x in map(lambda y: colour_rgb[y], image_data)]

    image.putdata(image_data)

    image.save(filename)

    return True


def export_multiple(series: List[pd.Series], filename: str, height: int = 16) -> bool:
    total_width = max(series, key=lambda x: x.size).size
    image = Image.new("RGB", (total_width, height * len(series)))

    image_data = []
    for serie in series:
        for _ in range(height):
            image_data.extend(serie.tolist())
            image_data.extend([0] * (total_width - serie.size))

    image_data = [x for x in map(lambda y: colour_rgb[y], image_data)]

    image.putdata(image_data)

    image.save(filename)

    return True


def export_2(series, filename):
    image = Image.new("RGB", (len(series), len(series[0])))

    # één lijst (eerste rij, dan tweede rij, dan ...)
    # image is een lisjt van kolommen -> omzetten

    big_sequ = []
    for j in range(len(series[0])):
        for i in range(len(series)):
            big_sequ.append(series[i][j])

    # ik moet meer kleurtjes hebben die niet overeenkomen met basen voor mijn prentjes
    import copy
    rgb_copy = copy.copy(colour_rgb)
    rgb_copy[-1] = (50, 50, 60)
    rgb_copy[-2] = (200, 100, 80)
    rgb_copy[-3] = (40, 20, 170)

    image_data = [x for x in map(lambda y: rgb_copy[y], big_sequ)]

    #image_data = [x for x in map(lambda y: dict(colour_rgb, **{-1: (100, 100, 30)})[y], big_sequ)]

    image.putdata(image_data)

    image.save(filename)

    return True


def main():
    import sys
    import argparse

    from .csvfile import CSVFile

    parser = argparse.ArgumentParser(description="Convert a sequence CSV to an image")
    parser.add_argument("file", type=str, help="The file to convert")
    parser.add_argument("image", type=str, help="The base filename of the output image")
    parser.add_argument("--height", default=16, type=int, required=False, help="The image height")

    args = parser.parse_args(sys.argv[1:])

    def processing(filename: str, column: str):
        df = pd.read_csv(filename, index_col=False, usecols=["Time", column], na_values="-")
        df = df.fillna(0)

        export(df[column], f"{args.image}_{column}.png", height=args.height)

    CSVFile(args.file).process(processing)


if __name__ == "__main__":
    main()
