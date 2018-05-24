from bs4 import BeautifulSoup
from datetime import datetime
import sys
sys.path.insert(0, '/Users/jeremypattison/LargeDocument/scripts/hansardScripts')
import hansardReading

def normaliseTranscript(transcriptDic):
    raw = transcriptDic["content"]
    normalised = hansardReading.keepCommonText(raw)
    transcriptDic["normalised"] = normalised
    return transcriptDic

def normaliseAndStem(transcriptDic):
    normaliseTranscript(transcriptDic)
    transcriptDic["normalised"] = hansardReading.stemParagraph(transcriptDic["normalised"])
    




def getAttributes(soup):
    transcriptIds = soup.find_all("span", {"class": "data-transcript-id"})
    dates = soup.find_all("span", {"class": "data-release-date"})
    transcriptTypes = soup.find_all("span", {"class": "data-release-type"})
    #print transcriptIds
    if len(transcriptIds) > 1:
        print("more than one transcriptIds")
        print transcriptIds
    transcriptId = transcriptIds[0].text
    if len(dates) > 1:
        print("more than one date")
        print dates
    dateString = dates[0].text
    tranDate = datetime.strptime(dateString, '%d/%m/%Y')
    if len(transcriptTypes) > 1:
        print "more than one transcript type"
        print transcriptTypes
    tranType = transcriptTypes[0].text
    return (transcriptId, tranDate, tranType)

def transcriptToDic(filepath):

    input_file = open(filepath)
    soup = BeautifulSoup(input_file, 'html.parser')
    fileMap = {}
    attributes = getAttributes(soup)
    fileMap["data-transcript-id"] = attributes[0]
    fileMap["data-release-date"] = attributes[1]
    fileMap["data-release-type"] = attributes[2]
    tranType = attributes[2]


    # if not tranType in tranTypes:
    #     print tranType
    #     tranTypes[tranType] = 0
    # tranTypes[tranType] +=1

    content = soup.find_all("div", {"class": "relative-required data-content"})[0].text

    lines = content.split("\n")
    content = " ".join(lines)
    if "end" in lines[-1].lower():
        lines = lines[0:-1]
    fileMap["content"] = content

    return fileMap




