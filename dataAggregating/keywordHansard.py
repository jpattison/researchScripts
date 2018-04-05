"""
The purpose of this is to go through all hansard data and return statistics from it.

Done:
1) Read old hansard
2) Build regex counter 
3) create polymorphic solution for old hansard
4) Same for new

TODO:


5) Export as JSON
6) Seperate new between question and other time
7) Seperate old
8) Merge new and old reader

"""

import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

import freq

HANSARD_LOCATION = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard"





def getDebateText(current, element):
    if element.text is not None:
        current = current + element.text
    for child in element:
        current = getDebateText(current, child)
    return current

def freqAggregator(listOfDics):
    """
    Given a list of dictionaries. 
    """
    output = {}

    for dic in listOfDics:
        for key in dic:
            if not key in output:
                output[key] = 0
            output[key] += dic[key]
    return output





def readHansard(startString, endString, oldReader, newReader, freqCounter, *args):
    """
    note last year not inclusive

    """
    yearStart =int(startString)
    yearEnd = int(endString)

    if(yearStart < 1998 or yearEnd > 2018 or yearStart>=yearEnd):
        raise ValueError("year out of range")

    
    folders = [str(x) for x in range(yearStart,yearEnd)] # note 2011 folder is not called 2011 hence only go up to 2010
    if yearStart < 2011 and 2011 < yearEnd:
        folders.append('2011_before_april') # represents 2011 for old data

    
    output = {}

    for folder in folders:
        input_directory = HANSARD_LOCATION+"/{0}".format(folder)
        for filename in os.listdir(input_directory):
            if not '.xml' in filename or len(filename)>14: # find neater way probably regex
                continue

            file_path = input_directory+'/'+filename
            input_file = open(file_path)
            tree = ET.parse(input_file)
            root = tree.getroot()    
            
            
            if filename in output and filename != "2011":
                raise ValueError("duplicate name detected : {0}".format(filename))

            if folder == "2011_before_april" or int(folder)<2011:
                #print "old reader"

                text = oldReader(root)
            else:
                text = newReader(root)

            

            freqCount = freqCounter(text, *args)

            # use date in format of dd/mm/yy as key, need to parse and translate the date

            stringDate = filename[:-4] #by removing last 4 we end up with the dates in YYYY-mm-dd
            date = datetime.strptime(stringDate, '%Y-%m-%d')
            keyword = date.strftime('%d-%m-%Y')
            
            if keyword in output:
                raise ValueError("duplicate name detected : {0}".format(filename))
            

            output[keyword] = freqCount


            
    return output


def newReader(root):
    # read a document and return relevent bits as one continious string

    output = ""


    #para.text
    for para in root.iter('talk.text'):

        text = getDebateText('', para)
        text = re.sub('(\s|$|\n)+',' ',text)

        output += freq.remove_non_ascii(text)

    return output


def oldReader(root):
    # read a document and return relevent bits as one continious string

    output = ""


    #para.text
    for para in root.iter('para'):

        text = getDebateText('', para)
        text = re.sub('(\s|$)+',' ',text)

        output += freq.remove_non_ascii(text)

    return output


# ausDescription = "checking for austerity"
# ausRegex = re.compile('[Aa]usterity')

# budDescription = "checking for budget"
# budRegex = re.compile('[Bb]udget')

# budCutDescription = "checking for budget cuts"
# budCutRegex = re.compile('[Bb]udget.{0,20}cut')

# regList = [[ausDescription, ausRegex], [budDescription, budRegex], [budCutDescription, budCutRegex]]
# frequencies =  readHansard("2010","2012", oldReader, newReader,freq.getRegFrequency, regList)


# organised = freq.oraganiseByKeyword(frequencies)

# print freq.aggregateByMonth(organised)
