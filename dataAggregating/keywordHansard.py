"""
The purpose of this is to go through all hansard data and return statistics from it.

Done:
1) Read old hansard
2) Build regex counter 
3) create polymorphic solution for old hansard


TODO:

4) Same for new
5) Export as JSON
6) Seperate new between question and other time
7) Seperate old

"""

import os
import re
from unidecode import unidecode
import xml.etree.ElementTree as ET


HANSARD_LOCATION = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard"


def remove_non_ascii(text):

    #print(text)

    if text:
        return unidecode(text)
    return None


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

def getRegFrequency(text, regInfos):
    # regInfo must be of from [ [description,regexPattern], ..... [description,regexPattern]]
    output = {}
    

    for description, regPattern in regInfos:

        #print speech
        matches = regPattern.findall(text)
        if matches is None:
            frequency = 0
        else:
            frequency = len(matches)

        if description in output:
            raise ValueError("duplicate description detected : {0}".format(description))
        
        output[description] = frequency
    return output



def readHansard(yearStart, yearEnd, oldReader, newReader, freqCounter, *args):
    """
    note last year not inclusive

    """


    if(yearStart < 1998 or yearEnd > 2018 or yearStart>=yearEnd):
        raise ValueError("year out of range")

    
    folders = [str(x) for x in range(yearStart,yearEnd)] # note 2011 folder is not called 2011 hence only go up to 2010
    if yearStart < 2011 and 2011 < yearEnd:
        folders.append('2011_before_april') # represents 2011 for old data

    
    output = {}

    for folder in folders:
        input_directory = HANSARD_LOCATION+"/{0}".format(folder)
        for filename in os.listdir(input_directory):
            if not '.xml'in filename:
                continue

            file_path = input_directory+'/'+filename
            input_file = open(file_path)
            tree = ET.parse(input_file)
            root = tree.getroot()    
            
            frequencyList = [] # list of dictonaries for individual speeches
            
            if filename in output and filename != "2011":
                raise ValueError("duplicate name detected : {0}".format(filename))

            if folder == "2011_before_april" or int(folder)>2011:
                text = oldReader(root)
            else:
                text = newReader(root)

            
            print filename
            freq = freqCounter(text, *args)


            # due to two 2011 folders we need to make sure they are combined
            if folder == "2011_before_april":
                combined = [freq]
                if "2011" in output:
                    combined.append(output["2011"])
                frequencyCombined = freqAggregator(frequencyList)
                output["2011"] = frequencyCombined   

            elif folder == "2011" and "2011" in output:
                combined = [output["2011"], freq]
                frequencyCombined = freqAggregator(frequencyList)
                output["2011"] = frequencyCombined                 

            else:
                output[filename] = freq

            frequencyCombined = freqAggregator(frequencyList)
            
    return output


def newReader(root):
    # read a document and return relevent bits as one continious string

    output = ""


    #para.text
    for para in root.iter('talk.text'):

        text = getDebateText('', para)
        text = re.sub('(\s|$|\n)+',' ',text)

        output += remove_non_ascii(text)

    return output


def oldReader(root):
    # read a document and return relevent bits as one continious string

    output = ""


    #para.text
    for para in root.iter('para'):

        text = getDebateText('', para)
        text = re.sub('(\s|$)+',' ',text)

        output += remove_non_ascii(text)

    return output


ausDescription = "checking for austerity"
ausRegex = re.compile('[Aa]usterity')

budDescription = "checking for budget"
budRegex = re.compile('[Bb]udget')

budCutDescription = "checking for budget cuts"
budCutRegex = re.compile('[Bb]udget.{0,20}cut')

regList = [[ausDescription, ausRegex], [budDescription, budRegex], [budCutDescription, budCutRegex]]
print readHansard(2010,2012, oldReader, newReader, getRegFrequency, regList)

