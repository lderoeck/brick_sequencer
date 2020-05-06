from brick_sequencer.BaseGuesser import *
import brick_sequencer.BaseCaller
from brick_sequencer.TimeCalculator import *

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
    #files.remove('Experiment10X_WWWWWWWWBBGGBBBYBYGYRRRBGGYGRGGWWWWWWWW.csv' )
    return files

def getAccuracy(dir, files):
    """

    :param dir: directory to find training files
    :param files: training files
    :return: average accuracy of all training files
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
            writeToFile.write("Correct Sequence: " + str(sequence.upper())+"\n")

            df = pd.read_csv(file, index_col=False, usecols=["Time", column])
            df = df.replace('-', 0.0)
            if df["Time"].dtypes != float:
                df["Time"] = pd.to_numeric(df["Time"], errors='coerce')
            if df[column].dtypes != float:
                df[column] = pd.to_numeric(df[column], errors='coerce')

            time = TimeCalculator().calc_time(df[column].to_numpy())

            dfRes = BaseGuesser.sequence(brick_sequencer.BaseCaller.dropNonSequence(df), time)
            writeToFile.write("Guessed sequence: ")
            for i,j in dfRes.iterrows():
                writeToFile.write(convertColor(j[0]))
            writeToFile.write("\n")
            writeToFile.write("Column: " + column + "\n")
            accuracy = calculateAcurracyRun(sequence, dfRes)
            writeToFile.write("Accuracy: "+str(accuracy)+"\n\n")

            totalScore += accuracy
            columnNumber += 1

    writeToFile.write("\n Average accuracy: " + str(totalScore/totalRuns))
    return totalScore/totalRuns

def calculateAcurracyRun(expected, dfRes):
    """

    :param expected: expected sequence
    :param dfRes: dataframe of guessed sequence
    :return: accuracy of single run
    """
    right = 0
    total = 0
    index = 0
    toMatchIndex = 0
    sameColorCounter = 0
    lastColor = None
    rowCount = len(dfRes.index)
    if rowCount> len(expected):
        runLength = rowCount
        while index < runLength:
            if index < rowCount and toMatchIndex < len(expected):
                rowData = dfRes.loc[index, :]


                if isSameColor(expected[toMatchIndex], rowData[0]):
                    right += 1
                elif toMatchIndex + 1 < len(expected) and isSameColor(expected[toMatchIndex + 1], rowData[0]):
                    right += 1
                    total += 1
                    toMatchIndex += 1
                else:
                    safeIndex = toMatchIndex
                    rowData2 = dfRes.loc[index+1, :]
                    while sameColorCounter>0:
                        safeIndex +=1
                        # temp1 = safeIndex
                        # temp2 = (expected[safeIndex])
                        # temp3 = rowData[0]
                        if safeIndex < len(expected) and isSameColor(expected[safeIndex], rowData[0]):
                            right+=1
                            total += (safeIndex-toMatchIndex)
                            toMatchIndex = safeIndex
                            break
                        elif safeIndex < len(expected) and index<rowCount and isSameColor(expected[safeIndex], rowData2[0]):
                            right += 1
                            total += (safeIndex - toMatchIndex)
                            index+=1
                            toMatchIndex = safeIndex
                            break
                        sameColorCounter -=1
                if rowData[0] == lastColor:
                    sameColorCounter += 1
                else:
                    sameColorCounter = 0
                lastColor = rowData[0]

            total += 1
            index += 1
            toMatchIndex += 1
    else:
        runLength = len(expected)
        while toMatchIndex < runLength:
            if index < rowCount and toMatchIndex < len(expected):
                rowData = dfRes.loc[index, :]
                if isSameColor(expected[toMatchIndex], rowData[0]):
                    right += 1
                elif toMatchIndex + 1 < len(expected) and isSameColor(expected[toMatchIndex + 1], rowData[0]):
                    right += 1
                    total += 1
                    toMatchIndex += 1
                else:
                    safeIndex = toMatchIndex
                    if index+1< rowCount:
                        rowData2 = dfRes.loc[index+1, :]
                    while sameColorCounter>0:
                        safeIndex +=1
                        # temp1 = safeIndex
                        # temp2 = (expected[safeIndex])
                        # temp3 = rowData[0]
                        if safeIndex < len(expected) and isSameColor(expected[safeIndex], rowData[0]):
                            right+=1
                            total += (safeIndex-toMatchIndex)
                            toMatchIndex = safeIndex
                            break
                        elif safeIndex < len(expected) and index+1<rowCount and isSameColor(expected[safeIndex], rowData2[0]):
                            right += 1
                            total += (safeIndex - toMatchIndex)
                            index+=1
                            toMatchIndex = safeIndex
                            break
                        sameColorCounter -=1
                if rowData[0] == lastColor:
                    sameColorCounter += 1
                else:
                    sameColorCounter = 0
                lastColor = rowData[0]

            total += 1
            index += 1
            toMatchIndex += 1

    return right/total

def isSameColor(exp, res):

    """

    :param exp: expected base
    :param res: guessed base
    :return: True if guessed and expected base are the same
    """
    res = convertColor(res)

    if exp.capitalize() == res:
        return True
    else:
        return False

def convertColor(res):
    """

    :param res: color code of guessed base
    :return: capital letter of base
    """
    """
    
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
        return "0"
    return res


if __name__ == "__main__":
    writeToFile = open("../accuracyResults/Result2.txt", "w")
    dir = "../trainingData/"
    getAccuracy(dir, getFiles(dir))
    writeToFile.close()
