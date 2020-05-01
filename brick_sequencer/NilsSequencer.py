import pandas as pd
from image import export_2

collist = ["0", "1", "b", "g", "y", "r", "W", "7"]

def csv_to_list(fname):
    df = pd.read_csv(fname, sep=",")

    arrays = df.transpose().to_numpy()

    arrays_py = []
    for i in range(len(arrays)-1):
        ls = []

        for elem in arrays[i]:
            try:
                ls.append(int(float(elem)))
            except:
                ls.append(0)

        arrays_py.append(ls)

    return arrays_py


def find_4white(sequence, start_index, width = 8):
    # 1) begin zoeken van de eerstvolgende witte basen
    start = start_index
    while start < len(sequence) - width:
        if sequence[start:start + width].count(6) == width:
            break
        start += 1

    # 2) einde zoeken van de eerstvolgende witte basen
    end = start
    while end < len(sequence) - width:
        if sequence[end:end + width].count(6) <= width/2:
            break
        end += 1

    return start, end


# werkt niet goed want zitten echt grote fouten, soms duurt een base 0.62s, en erna een andere base 0.4s, of 2 basen 0.7s samen
def try_1(x, speed):



    for sequence in x:
        index_pos = []

        start_w1, end_w1 = find_4white(sequence, 0)
        start_w2, end_w2 = find_4white(sequence, end_w1+1)

        print("w1:", start_w1, end_w1)
        print("w2:", start_w2, end_w2)
        speed_guess1 = (end_w1 - start_w1) / 100 / 4
        speed_guess2 = (end_w2 - start_w2) / 100 / 4

        print("speed_guesses:", speed_guess1, speed_guess2)  # ter info

        using_speed = (speed + speed_guess1 + speed_guess2)/3
        print("-> using speed", using_speed)
        scans_per_base = int(100*using_speed)



        upper_calib_limit = int(1.3 * scans_per_base)
        lower_calib_limit = int(0.8 * scans_per_base)


        # willen beginnen in het midden van de eerste base na de 4 witte
        pos = int(end_w1 + scans_per_base/2)

        #print("starting at position", pos, "with color", sequence[pos])

        while pos < start_w2:
            color = sequence[pos]

            #print("col", color)

            # hercalibreren: zoeken naar begin/einde van huidige base, zolang som van afstanden +- kleiner is dan lengte van
            # 1 base, zitten we niet in een herhaling

            base_start = pos
            while base_start > end_w1:
                if sequence[base_start-1:base_start+2].count(color) <= 1:
                    break
                base_start -= 1

            base_end = pos
            while base_end < start_w2:
                if sequence[base_end-1:base_end+2].count(color) <= 1:
                    break
                base_end += 1

            base_length = base_end - base_start

            print("base", collist[color], "at", pos, ": starts at", base_start, "and ends at", base_end, "-> len", base_length,
                  "(", lower_calib_limit, upper_calib_limit, ")")

            if base_length < lower_calib_limit:
                print("base", collist[color], "too short: reject!")
                pos = int(base_end + scans_per_base/2)  # naar volgende base proberen geraken
                continue

            index_pos.append(pos) # toevoegen

            if base_length > upper_calib_limit:
                print("base", collist[color], "too long: can't calibrate!")
                pos += scans_per_base # naar volgende base gaan
                continue

            # we willen in het midden van de base blijven -> we willen dat base_end-pos en pos-base_start ongeveer gelijk zijn
            print("calibrating pos", pos, "to", (base_start + base_end)//2)
            pos = (base_start + base_end)//2
            pos += scans_per_base # naar volgende base gaan


        print("-> pick bases from", index_pos)
        basestr = ""
        for index in index_pos:
            basestr += collist[sequence[index]]

        print("-> \"" + basestr + "\"")

        #break






def try_2(x, base_speed):
    # afbeelding
    base_height = 40   # hoogte voor de basen
    lower_height = 40  # pijltje eronder
    sep_height = 20    # plek tussen pijltje en base van volgende sequence
    # -> image_width = max(len(sequence) for sequence in x)
    # -> image_height = len(x)*(base_height + lower_height + sep_height) - sep_height
    image = []  # lijst van kolommen
    image_height = len(x)*(base_height + lower_height + sep_height) - sep_height

    for i in range(max(len(sequence) for sequence in x)):
        column = [-1 for j in range(image_height)]

        for j in range(len(x)):
            if len(x[j]) < i:
                continue

            for k in range(base_height):
                column[j*(base_height + lower_height + sep_height) + k] = x[j][i]



        image.append(column)



    start_w1 = []
    end_w1 = []
    start_w2 = []
    end_w2 = []
    speed = []
    scans_per_base = []

    for sequence in x:
        s_start_w1, s_end_w1 = find_4white(sequence, 0)
        s_start_w2, s_end_w2 = find_4white(sequence, s_end_w1+1)

        start_w1.append(s_start_w1)
        end_w1.append(s_end_w1)
        start_w2.append(s_start_w2)
        end_w2.append(s_end_w2)



        #print("w1:", s_start_w1, s_end_w1)
        #print("w2:", s_start_w2, s_end_w2)
        speed_guess1 = (s_end_w1 - s_start_w1) / 100 / 4
        speed_guess2 = (s_end_w2 - s_start_w2) / 100 / 4

        #print("speed_guesses:", speed_guess1, speed_guess2)  # ter info

        speed.append((base_speed + speed_guess1 + speed_guess2)/3)
        scans_per_base.append(int(100*speed[-1]))

    print("start_w1", start_w1)
    print("  end_w1", end_w1)
    print("start_w2", start_w2)
    print("  end_w2", end_w2)
    print("   speed", speed)
    print("scans/ba", scans_per_base)

    upper_calib_limit = [int(1.3 * s) for s in scans_per_base]
    lower_calib_limit = [int(0.8 * s) for s in scans_per_base]


    pos = [end_w1[i] + scans_per_base[i]//2 for i in range(len(x))]

    out_sequ = []

    while True:
        print("position", pos)
        pick = [x[i][pos[i]] for i in range(len(x))]
        print("    pick", [collist[c] for c in pick])

        if pick.count(pick[0]) == len(x):
            # elke sequence pakt zelfde base -> ok
            out_sequ.append(collist[pick[0]])

            # posities verhogen, calibreren
            for i in range(len(x)):
                base_start = pos[i]
                color = x[i][pos[i]]

                while base_start > end_w1[i]:
                    if x[i][base_start - 1:base_start + 2].count(color) <= 1:
                        break
                    base_start -= 1

                base_end = pos[i]
                while base_end < start_w2[i]:
                    if x[i][base_end - 1:base_end + 2].count(color) <= 1:
                        break
                    base_end += 1

                base_length = base_end - base_start

                print("base", collist[color], "at", pos[i], ": starts at", base_start, "and ends at", base_end, "-> len",
                      base_length,
                      "(", lower_calib_limit[i], upper_calib_limit[i], ")")

                if base_length < lower_calib_limit[i]:
                    print("base", collist[color], "too short: reject!")
                    pos[i] = int(base_end + scans_per_base[i]/2)  # naar volgende base proberen geraken
                    continue

                if base_length > upper_calib_limit[i]:
                    print("base", collist[color], "too long: can't calibrate!")
                    pos[i] += scans_per_base[i]  # naar volgende base gaan
                    continue

                # we willen in het midden van de base blijven -> we willen dat base_end-pos en pos-base_start ongeveer gelijk zijn
                print("calibrating pos", pos[i], "to", (base_start + base_end) // 2)
                pos[i] = (base_start + base_end) // 2
                pos[i] += scans_per_base[i]  # naar volgende base gaan
        else:
            print("disagree: break")
            break



    print("->", out_sequ)

    export_2(image, "out.png")




def main():
    #fname = "../trainingData/WWWWbbbbbbbbbbWWWW_speed5.csv"
    fname = "../trainingData/WWWWyggbgrbrbygyrbrrWWWW_speed5.csv"
    x = csv_to_list(fname) # lijst van lijsten

    speed = 0.5  # seconden per base   TODO niet meer hardcoden


    #scans_per_base = int(100*speed)   # scans/s * s/base -> scans/base
    #try_1(x, speed)
    try_2(x, speed)




if __name__ == "__main__":
    main()
