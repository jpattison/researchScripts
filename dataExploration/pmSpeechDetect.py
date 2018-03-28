"""
Count frequency of a specific topic for PM transcripts between specific dates.

"""


from unidecode import unidecode
from bs4 import BeautifulSoup
import os
from datetime import datetime
import re
import shutil

SPEECHLOCATION = "/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/xml"
LOCATION2013TO2016 = "/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/2003to2015"

def remove_non_ascii(text):

    #print(text)

    if text:
        return unidecode(text)
    return None
    #return unidecode(unicode(text, encoding = "utf-8"))

def readTranscript(filename):
    """
    Returns the date and the body
    """

    input_file = open(filename)
    soup = BeautifulSoup(input_file, 'html.parser')

    dates = soup.find_all("span", {"class": "data-release-date"})

    speechBs4 = soup.find_all("div", {"class": "transcript-body"})
    speech = str(speechBs4)
    #print type(speech) #run remove_non_ascii?

    if len(dates) > 1:
        print "unexpected date data {0}".format(filename)
    elif dates == []:
        print "empty date in {0}".format(filename)
        return None, speech
    dateString = dates[0].text    

    datetime_object = datetime.strptime(dateString, '%d/%m/%Y')
    # convert date to timestgamp
    # format dd/mm/yyyy
    return datetime_object, speech

def getFrequency(speech, regPatterns):
    frequency = 0

    for regPattern in regPatterns:
        #print speech
        matches = regPattern.findall(speech)
        if matches is None:
            continue
        frequency += len(matches)

    return frequency

def makeZeroList(dateStart, dateEnd):
    zeroList = []
    for year in range(dateStart.year, dateEnd.year):
        yearList = []
        for i in range(0,12):
            yearList.append(0)
        zeroList.append(yearList)
    return zeroList


def countFrequency(speech, regPattern):
    matches = regPattern.findall(speech)
    if matches is None:
        return 0
    return len(matches)

def detectKeywords(sourceLocation, regPatterns, dateStart, dateEnd):
    """
    Check speeches inbetween time period. For each regPattern returns a 
    month by month breakdown of counts
    """
    count = 0
    frequencyCount = []

    fileCount = 0
    
    solution = {}
    for regPattern in regPatterns:
        description = regPattern[1]
        solution[description] = makeZeroList(dateStart, dateEnd)

    makeZeroList(dateStart, dateEnd)

    for filename in os.listdir(sourceLocation):
        fileCount += 1
        if fileCount%1000 == 0:
            print "{0} files read".format(fileCount)
        filePath = sourceLocation+'/'+filename
        if not 'transcript-' in filename:
            continue
        date, speech = readTranscript(filePath)
        #frequency = getFrequency(speech, regPatterns)
        if date >= dateStart and date <=dateEnd:
            yearCounter = date.year - dateStart.year
            monthCounter = date.month -1 # reduce by 1 for index logic
            #print yearCounter
            #print monthCounter
            for regPattern in regPatterns:
                #print solution[regPattern]
                #print solution[regPattern][yearCounter]
                #print solution[regPattern][yearCounter][monthCounter]
                expression = regPattern[0]
                description = regPattern[1]
                solution[description][yearCounter][monthCounter] += countFrequency(speech, expression)
    return solution


def filterFiles(sourceLocation, dateStart, dateEnd, destinationFolder):
    """
    Go through all files in folder and send any within specific dates to destination
    """
    try:
        os.stat(destinationFolder)
    except:
        os.mkdir(destinationFolder)

    for filename in os.listdir(sourceLocation):
        filePath = sourceLocation+'/'+filename
        
        if os.path.isdir(filePath) or not 'transcript-' in filename:
            continue
        
        date, speech = readTranscript(filePath)

        
        if date >= dateStart and date <=dateEnd:
            shutil.copy2(filePath, destinationFolder)



ausDescription = "checking for austerity"
ausRegex = re.compile('[Aa]usterity')

budDescription = "checking for budget"
budRegex = re.compile('[Bb]udget')

budCutDescription = "checking for budget cuts"
budCutRegex = re.compile('[Bb]udget.{0,20}cut')

startDate = datetime.strptime("01/01/2003", '%d/%m/%Y') #change to 2003
endDate = datetime.strptime("01/01/2016", '%d/%m/%Y')

# TODO: dont use regex expression as key, at least at moment its unreadable and its seems pretty poor practice
results = detectKeywords(LOCATION2013TO2016, [[ausRegex, ausDescription], [budRegex, budDescription],
    [budCutRegex, budCutDescription]
    ], startDate, endDate)

for keyWord in results:
    print keyWord
    print results[keyWord]
    for year in range(0,len(results[keyWord])):
        print year + startDate.year
        total = 0
        #print results[keyWord][year]
        for month in results[keyWord][year]:
            total += month
        print total

#filterFiles(SPEECHLOCATION, startDate, endDate, SPEECHLOCATION+"/2003to2015")