import os
import sys
from environment import OSEnv

def convertDir(dirName):
    print("Converting " + str(len(os.listdir(dirName))) + " files")
    counter = 1

    if not checkForConversionExecutable():
        print("Cannot find path to ffmpeg")
        return
    for file in os.listdir(dirName):
        if not checkForBadCharacters(file):
            file = renameFile(dirName, file)

        try:
            conversionResult = convert("./" + dirName + "/" + file)
            if conversionResult == 0:
                os.remove(dirName + "/" + file)
                print(str(counter) + " Converted " + file)
                counter += 1
            else:
                print("Failed to convert " + file)
        except UnicodeEncodeError:
            print("Failed to convert because the name of the file: UnicodeEncodeError")
            continue
    print("After conversion: " + str(len(os.listdir(dirName))) + " files")
    if os.path.isfile("conversion.log"):
        os.remove("conversion.log")


def checkForConversionExecutable():
    if os.path.isfile("ffmpeg-3.3-64bit-static/ffmpeg"):
        return True
    else:
        return False

def clearDir(dirName):
    for file in os.listdir(dirName):
        if not isMp3(file):
            os.remove(file)


def runCommand(origFile, convertedFile):
    command = "ffmpeg-3.3-64bit-static/ffmpeg -i " + origFile + " " + convertedFile + " 2>> conversion.log"
    return os.system(command)


def isMp3(fileName):
    return getExtension(fileName) == "mp3"


def getExtension(fileName):
    parts = fileName.split('.')
    return parts[len(parts) - 1]


def getConvertedFileName(fileName):
    extension = getExtension(fileName)
    newName = fileName.replace(extension, 'mp3')
    return "\"" + newName + "\""


def convert(fileName):
    if isMp3(fileName):
        print(fileName + " no need to convert")
        return
    convertedFileName = getConvertedFileName(fileName)
    fileName = "\"" + fileName + "\""
    return runCommand(fileName, convertedFileName)

def checkSystem():
    osName = sys.platform
    if "linux" in osName:
        return OSEnv.LINUX
    if "windows" in osName:
        return OSEnv.WINDOWS

def checkForBadCharacters(file):
    if '\'' in file or '`' in file or '’' in file or '‘' in file or '"' in file:
        return False
    return True

def renameFile(dirName, oldFile):
    if checkSystem() is OSEnv.LINUX:
        newFileName = oldFile.replace('\'', '')
        newFileName = newFileName.replace('`', '')
        newFileName = newFileName.replace('’', '')
        newFileName = newFileName.replace('‘', '')
        newFileName = newFileName.replace('"', '')
        operationResult = os.system("mv \"" + dirName + "/" + oldFile + "\" \"" + dirName + "/" + newFileName + "\"")
        if operationResult == 256:
            print("Failed to rename file with problematic name")
            return oldFile
        if operationResult == 0:
            print("[File renamed] " + newFileName)
        return newFileName
    else:
        print("Renaming not implemented for windows")
        return oldFile

