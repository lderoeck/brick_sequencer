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
    Colour.NONE.value: "none",
    Colour.BLACK.value: "black",
    Colour.BLUE.value: "blue",
    Colour.GREEN.value: "green",
    Colour.YELLOW.value: "yellow",
    Colour.RED.value: "red",
    Colour.WHITE.value: "white",
    Colour.BROWN.value: "brown"
}

# Short colour codes
colour_short = {
    Colour.NONE.value: "-",
    Colour.BLACK.value: "-",
    Colour.BLUE.value: "b",
    Colour.GREEN.value: "g",
    Colour.YELLOW.value: "y",
    Colour.RED.value: "r",
    Colour.WHITE.value: "w",
    Colour.BROWN.value: "-"
}

# Translate sequence data to RGB
colour_rgb = {
    Colour.NONE.value: (0, 0, 0),
    Colour.BLACK.value: (0, 0, 0),
    Colour.BLUE.value: (0, 0, 255),
    Colour.GREEN.value: (0, 255, 0),
    Colour.YELLOW.value: (255, 255, 0),
    Colour.RED.value: (255, 0, 0),
    Colour.WHITE.value: (255, 255, 255),
    Colour.BROWN.value: (120, 60, 60),
}


def translate(sequence: pd.DataFrame, translation: Optional[Dict[float, str]] = None) -> List[str]:
    if not translation:
        translation = colour_short

    return sequence.replace({"Colour": translation})["Colour"].tolist()
