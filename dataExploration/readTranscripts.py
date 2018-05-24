"""
Work in reading speeches by prime ministers 
"""

from unidecode import unidecode
from bs4 import BeautifulSoup
import sys
import os
sys.path.insert(0, '/Users/jeremypattison/LargeDocument/scripts/transcriptScripts')
import readTranscript


def remove_non_ascii(text):

    #print(text)

    if text:
        return unidecode(text)
    return None
    #return unidecode(unicode(text, encoding = "utf-8"))




def grabDistribution(inputDirectory):
    # method has to make a normalised document in "normalised"
    years = {}
    count = 0
    for filename in os.listdir(inputDirectory):
        fileMap = {}
        split = str(filename).split('.')

        if len(split) > 1 : # i.e. has a file extension
            #print split
            continue
        count +=1
        if count%100==0:
            print count
        file_path = inputDirectory+'/'+filename

        transcriptDic = readTranscript.transcriptToDic(file_path)
        year = transcriptDic["data-release-date"].year
        if not year in years:
            years[year] = 0
        [year]+=1
    print "cat"
    print years
        

        


grabDistribution('/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/xml/')