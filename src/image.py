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



def export_2(series, filename):
    image = Image.new("RGB", (len(series), len(series[0])))

    # één lijst (eerste rij, dan tweede rij, dan ...)
    # image is een lisjt van kolommen -> omzetten

    big_sequ = []
    for j in range(len(series[0])):
        for i in range(len(series)):
            big_sequ.append(series[i][j])

    image_data = [x for x in map(lambda y: colour_rgb[y], big_sequ)]

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
