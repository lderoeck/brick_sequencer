import pandas as pd
from PIL import Image

from .colour import colour_rgb


def export(series: pd.Series, filename: str) -> bool:
    image = Image.new("RGB", (series.size, 16))

    image_data = []
    for _ in range(16):
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