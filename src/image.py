import pandas as pd
from PIL import Image


def export(series: pd.Series, filename: str) -> bool:
    image = Image.new("RGB", (series.size, 16))

    image_data = []
    for _ in range(16):
        image_data.extend(series.tolist())

    # Translate sequence data to RGB
    colour_map = {
        0.0: (0, 0, 0),
        1.0: (0, 0, 0),
        2.0: (0, 0, 255),
        3.0: (0, 255, 0),
        4.0: (255, 255, 0),
        5.0: (255, 0, 0),
        6.0: (255, 255, 255),
        7.0: (120, 60, 60),
    }

    image_data = [x for x in map(lambda y: colour_map[y], image_data)]

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


    # Translate sequence data to RGB
    colour_map = {
        0: (0, 0, 0),
        1: (0, 0, 0),
        2: (0, 0, 255),
        3: (0, 255, 0),
        4: (255, 255, 0),
        5: (255, 0, 0),
        6: (255, 255, 255),
        7: (120, 60, 60),

        -1: (40, 60, 80)
    }

    image_data = [x for x in map(lambda y: colour_map[y], big_sequ)]

    image.putdata(image_data)

    image.save(filename)

    return True