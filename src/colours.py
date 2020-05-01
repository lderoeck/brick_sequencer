from typing import *

import pandas as pd

# Colour codes for the Lego Mindstorms EV3 Colour Sensor
#  See http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-stretch/sensor_data.html#lego-ev3-color-notes
colours = {
    0.0: "none",
    1.0: "black",
    2.0: "blue",
    3.0: "green",
    4.0: "yellow",
    5.0: "red",
    6.0: "white",
    7.0: "brown"
}

# Short colour codes
colours_short = {
    0.0: "-",
    1.0: "-",
    2.0: "b",
    3.0: "g",
    4.0: "y",
    5.0: "r",
    6.0: "w",
    7.0: "-"
}

# Translate sequence data to RGB
colours_rgb = {
    0.0: (0, 0, 0),
    1.0: (0, 0, 0),
    2.0: (0, 0, 255),
    3.0: (0, 255, 0),
    4.0: (255, 255, 0),
    5.0: (255, 0, 0),
    6.0: (255, 255, 255),
    7.0: (120, 60, 60),
}


def translate(sequence: pd.DataFrame, translation: Dict[float, str] = colours_short) -> List[str]:
    return sequence.replace({"Colour": translation})["Colour"].tolist()
