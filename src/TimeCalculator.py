import pandas as pd
import numpy as np
import re


class TimeCalculator:
    def __init__(self):
        self.white = np.vectorize(lambda x: x == "6.000" or x == 6)

    def calc_time(self, sequence, num_white=8, time_step=0.01, refined=False):
        """
        Calculates time needed to read a single base
        :param sequence: array (row) of sequence data
        :param num_white: amount of white bases present in sequence (start/end) (default: 8 bases)
        :param time_step: amount of time passed each step (default: 10ms)
        :param refined: filter out noise white (default: off)
        :return:
        """
        data = self.white(sequence) # kijken welke wit zijn
        # snelheid berekenen via tijd die de (default) 8 witte innemen
        # -> dit neemt alle witte (ook voor of na de eigenlijke start/einde)
        speed = np.floor(np.sum(data) / num_white) * time_step
        if not refined:
            return speed

        # poging beter te maken:
        # via weights zien dat we enkel de witten hebben die bij start/einde horen -> minimum gewicht
        # zo verliezen we wel een paar witten aan het begin/einde van het begin/einde -> paar extra
        # lijkt niet zo nuttig te zijn MAAR HET WAS WEL EEN GOEDE POGING!!
        extra = 5
        minimum_weight = 0.8

        weights = self.calc_weights(sequence, speed)

        data = []
        for i in range(len(sequence)):
            if (sequence[i] == "6.000" or sequence[i] == 6) and (weights[i] > minimum_weight):
                data.append(True)
            else:
                data.append(False)

        speed = np.floor((extra + np.sum(data)) / num_white) * time_step
        return speed


    def calc_weights(self, sequence, speed, area_factor=3):
        weight_area = int(np.ceil(area_factor / speed)) # voor element i wordt gekeken naar elementen i-area, i-area+1, ... i+area
        weights = []

        # weight: kijken hoeveel buren lijken op element
        # -> hoge weight in het midden van een base, lage weight bij de overgang tussen verschillende basen
        # 1 2 2 3
        # hier is de weight laag tussen 1 2  en tussen 2 3, niet tussen de middenste 2's

        for i in range(len(sequence)):
            numerator = 0
            denominator = 0
            j = -weight_area
            while j <= weight_area:
                if j == 0:
                    j += 1

                if (i + j) < 0:
                    j += 1
                    continue
                if (i + j) >= len(sequence):
                    j += 1
                    continue

                rel_weight = 1 + weight_area - abs(j)
                denominator += rel_weight
                if sequence[i] == sequence[i + j]:
                    numerator += rel_weight

                j += 1

            if denominator == 0:
                # kan normaal gezien niet behalve bij input lijst met maar één element in, of area_factor = 0
                weights.append(0.0)
            else:
                weights.append(numerator / denominator)


        #for i in range(len(sequence)):
        #    print(i, ":", sequence[i], ", weight", weights[i])


        return weights


    def read_csv(self, input_file: str):
        df = pd.read_csv(input_file, sep=",")

        arrays = df.transpose().to_numpy()

        for i in range(len(arrays) - 1):
            speed = self.calc_time(arrays[i])
            print("speed:", speed)


if __name__ == "__main__":
    t = TimeCalculator()
    t.read_csv("../trainingData/WWWWbbbbbbbbbbWWWW_speed5.csv")
    t.read_csv("../trainingData/WWWWggggggggggggWWWW_speed5.csv")
