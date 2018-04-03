import freq
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os



PMLOCATION = "/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/xml"

def getTranscript(filename):
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


def readTranscripts(yearStart, yearEnd, reader, freqCounter, *args):

    """
    Check speeches inbetween time period. 
    """
    dateStart = datetime.strptime(yearStart, '%Y')
    dateEnd = datetime.strptime(yearEnd, '%Y')
 

    output = {}

    fileCount = 0

    for filename in os.listdir(PMLOCATION):
        fileCount += 1
        if fileCount%1000 == 0:
            print "{0} files read".format(fileCount)
        filePath = PMLOCATION+'/'+filename
        if not 'transcript-' in filename:
            continue
        date, speech = getTranscript(filePath)
        #frequency = getFrequency(speech, regPatterns)
        if date >= dateStart and date <=dateEnd:
            freq = freqCounter(speech, *args)
            output[date.strftime('%d-%m-%Y')] = freq 
    return output



# ausDescription = "checking for austerity"
# ausRegex = re.compile('[Aa]usterity')

# budDescription = "checking for budget"
# budRegex = re.compile('[Bb]udget')

# budCutDescription = "checking for budget cuts"
# budCutRegex = re.compile('[Bb]udget.{0,20}cut')

# regList = [[ausDescription, ausRegex], [budDescription, budRegex], [budCutDescription, budCutRegex]]



# frequencies = readTranscripts("2011", "2013", getTranscript ,freq.getRegFrequency, regList)
# print freq.oraganiseByKeyword(frequencies)

