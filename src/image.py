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
