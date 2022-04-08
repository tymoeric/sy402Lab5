

import csv
from datetime import date
import hashlib

import os
from posixpath import dirname



class File:
    def __init__(self, hash, path, observeDate):
        self.hash = hash
        self.path = path
        self.observeDate = observeDate
    
    def __str__(self):
        return "File: " + self.hash + "\tPath:" + self.path + "\tObersved On:" + str(self.observeDate)

class ChangedFile:
    def __init__(self, hash, oldPath, newPath, observeDate):
        self.hash = hash
        self.oldPath = oldPath
        self.newPath = newPath
        self.observeDate = observeDate

    def __str__(self):
        return "Modified File:" + self.hash + "\tOld Path:" + self.oldPath + "\tNew Path:" + self.newPath


fileDict = {}
changedFiles = {}
newFiles = {}
today = date.today()


def importKnown():
    with open('files.csv') as csvFile:
        cReader = csv.reader(csvFile, delimiter=',')
        for row in cReader:
            fileDict[row[0]] = File(row[0], row[1], row[2])
    return

def saveKnown():
    with open('files.csv', 'w') as csvFile:
        cWriter = csv.writer(csvFile, delimiter=",")
        for file in list(fileDict.values()):
            # print(file)
            cWriter.writerow([file.hash, file.path, file.observeDate])

def checkFile(filePath):
    hash = hashlib.sha256(open(filePath, 'rb').read()).hexdigest()
    if hash in fileDict: # File found!
        originalPath = fileDict[hash].path
        originalDate = fileDict[hash].observeDate
        if originalPath != filePath: # File Moved!
            changedFiles[hash] = ChangedFile(hash, originalPath, filePath, today) # Add to the list of changed files
            fileDict[hash] = File(hash, filePath, today) # Overwrite original file record          
    else:
        newFiles[hash] = File(hash, filePath, today) # Add to the list of new Files
        fileDict[hash] = File(hash, filePath, today) # Add to the main list of Files



def doScan():
    ignoreDirs = ["dev", "proc", "run", "sys", "tmp", "var", "share", "lib"]
    

    for root, dirs, files in os.walk("/", topdown=True):
        print("Checking " + root)
        [dirs.remove(d) for d in dirs if d in ignoreDirs]
	
        for file in files:
            # print(dirName)
            # print(os.path.join(dirName, file))
            try:
                checkFile(os.path.join(root,file))
            except:
                print("An exception occured")
            

    return


def main():
    
    print("Import list of files...")
    importKnown()
    
    print("Check for Changes...")
    doScan()

    print("Files Modified since last scan: ")
    for file in list(changedFiles.values()):
        print(file)
    
    print("New Files created since last scan: ")
    for file in list(newFiles.values()):
        print(file)

    print("Save file roster...")
    saveKnown()
    
    return


if __name__ == "__main__":
    main()
