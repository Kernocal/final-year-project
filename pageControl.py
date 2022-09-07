import os
from scraper import addPage, generateTime

def storePage(fileName, responseText, date):
    pathName = "archive/" + date + "/" + fileName + ".html"
    os.makedirs(os.path.dirname(pathName), exist_ok=True)
    with open(pathName, "w") as f:
        f.write(responseText.text)

def archivePage(name, fileData):#c
    time = generateTime()
    storePage(name, fileData, time[0])
    addPage(name, time[0], time[1])
    print("Archived page {0} at {1}.".format(name, time[1]))