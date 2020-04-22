from src.TimeCalculator import *

whiteThreshold = 10  # threshold to recognize the starting white block(s)

# Color Codes:
# 1 	black
# 2 	blue
# 3 	green
# 4 	yellow
# 5 	red
# 6 	white
# 7 	brown

def dropBeforeSequence(df):
    index  = 0
    rowCount = len(df.index)
    whiteCounter = 0
    cutIndex = 0
    while index < rowCount:
        rowData = df.loc[index, :]
        if rowData[1] == 6:
            if whiteCounter == 0:
                cutIndex = index
                temp = rowData[0]
            whiteCounter += 1
            if whiteCounter == 10:
                return df.iloc[cutIndex: , :]
        else:
            whiteCounter = 0
        index += 1


if __name__ == "__main__":
    column = "Colour_p4_01"
    file = "../trainingData/WWWWyrgbyyrrggbbyyyrrrgggbbbyyyyrrrrggggbbbbWWWW_speed5.csv"
    df = pd.read_csv(file, index_col=False, usecols=["Time", column])
    print(dropBeforeSequence(df))
