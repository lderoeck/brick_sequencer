from src.BaseGuesser import *
import src.BaseCaller
from src.TimeCalculator import *

from os import walk

def getFiles(dir):
    """"
        gets all the files from a directory to guess the bases for
        :dir: directory of test files
    """
    files = []
    for (dirpath, dirnames, filenames) in walk(dir):
        files.extend(filenames)
        break
    files.remove('README.txt')  # README is not a file to evaluate
    return files

def getAccuracy(dir, files):
    """"
        gets the total accuracy of all the files in the given directory
        :dir: directory of test files
        :files: files to test
    """
    totalRuns = 0
    totalScore = 0
    for file in files:
        if file.find("_") != -1:
            sequence = file.split("_")[0]
            if sequence[0] != "W":
                sequence = file.split("_")[1].split(".csv")[0]
        else:
            sequence=file.split("speed")[0]
        file = dir + file
        cols = pd.read_csv(file, nrows=1).columns.tolist()
        columnNumber = 1
        while columnNumber < len(cols):
            totalRuns += 1
            column = cols[columnNumber]
            print(sequence)
            df = pd.read_csv(file, index_col=False, usecols=["Time", column])
            df = df.replace('-', 0.0)
            if df["Time"].dtypes != float:
                df["Time"] = pd.to_numeric(df["Time"], errors='coerce')
            if df[column].dtypes != float:
                df[column] = pd.to_numeric(df[column], errors='coerce')

            time = TimeCalculator().calc_time(df[column].to_numpy())

            #print(time)

            dfRes = BaseGuesser.sequence(src.BaseCaller.dropNonSequence(df), time)
            accuracy = calculateAcurracyRun(sequence, dfRes)
            print(accuracy)
            print(dfRes)
            totalScore += accuracy
            columnNumber += 1
    print(totalScore/totalRuns)
    return totalScore/totalRuns

def calculateAcurracyRun(expected, dfRes):
    """"
        Calculates the accuracy of 1 rune
        :excepted: expected sequence in the form of a list
        :dfRes: guessed sequence in a pandas dataframe
    """
    right = 0
    total = 0
    index = 0
    rowCount = len(dfRes.index)
    if rowCount> len(expected):
        runLength = rowCount
    else:
        runLength = len(expected)
    while index < runLength:
        if index<rowCount and index<len(expected):
            rowData = dfRes.loc[index, :]
            if isSameColor(expected[index], rowData[0]):
                right +=1
        total +=1
        index += 1
    return right/total

def isSameColor(exp, res):
    """"
        :return: boolean True if the expected and the guessed color are the same, otherwise false
        # Color Codes:
        # 1 	black
        # 2 	blue
        # 3 	green
        # 4 	yellow
        # 5 	red
        # 6 	white
        # 7 	brown
    """
    if res == 2:
        res = "B"
    elif res == 3:
        res = "G"
    elif res == 4:
        res = "Y"
    elif res == 5:
        res = "R"
    elif res == 6:
        res = "W"
    else:
        return False

    if exp.capitalize() == res:
        return True
    else:
        return False


if __name__ == "__main__":
    dir = "../trainingData/"
    getAccuracy(dir, getFiles(dir))
