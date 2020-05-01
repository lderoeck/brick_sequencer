from typing import *
from enum import Enum

import pandas as pd


# Colour codes for the Lego Mindstorms EV3 Colour Sensor
#  See http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-stretch/sensor_data.html#lego-ev3-color-notes
class Colour(Enum):
    NONE = 0.0
    BLACK = 1.0
    BLUE = 2.0
    GREEN = 3.0
    YELLOW = 4.0
    RED = 5.0
    WHITE = 6.0
    BROWN = 7.0


colour_name = {
    Colour.NONE: "none",
    Colour.BLACK: "black",
    Colour.BLUE: "blue",
    Colour.GREEN: "green",
    Colour.YELLOW: "yellow",
    Colour.RED: "red",
    Colour.WHITE: "white",
    Colour.BROWN: "brown"
}

# Short colour codes
colour_short = {
    Colour.NONE: "-",
    Colour.BLACK: "-",
    Colour.BLUE: "b",
    Colour.GREEN: "g",
    Colour.YELLOW: "y",
    Colour.RED: "r",
    Colour.WHITE: "w",
    Colour.BROWN: "-"
}

# Translate sequence data to RGB
colour_rgb = {
    Colour.NONE: (0, 0, 0),
    Colour.BLACK: (0, 0, 0),
    Colour.BLUE: (0, 0, 255),
    Colour.GREEN: (0, 255, 0),
    Colour.YELLOW: (255, 255, 0),
    Colour.RED: (255, 0, 0),
    Colour.WHITE: (255, 255, 255),
    Colour.BROWN: (120, 60, 60),
}


def translate(sequence: pd.DataFrame, translation: Optional[Dict[float, str]] = None) -> List[str]:
    if not translation:
        translation = colour_short

    return sequence.replace({"Colour": translation})["Colour"].tolist()
