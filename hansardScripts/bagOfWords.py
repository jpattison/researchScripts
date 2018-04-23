import hansardReading
import xml.etree.ElementTree as ET
import re
import json
from sklearn.feature_extraction import DictVectorizer
import os

def singleDocumentToText(fileLocation, isNew):
    input_file = open(fileLocation)
    tree = ET.parse(input_file)
    if isNew:
        textArray = hansardReading.readNewText(tree.getroot())
    else:
        textArray = hansardReading.readOldText(tree.getroot())

    text = ""
    for element in textArray:
        text += element
    #text = re.sub('[\s\n\r]+',' ',text)
    text = hansardReading.returnOnlyText(text)
    return text


def singleDocumentToNormalised(fileLocation, isNew):
    input_file = open(fileLocation)
    tree = ET.parse(input_file)
    if isNew:
        textArray = hansardReading.readNewText(tree.getroot())
    else:
        textArray = hansardReading.readOldText(tree.getroot())

    text = ""
    for element in textArray:
        text += element
    #text = re.sub('[\s\n\r]+',' ',text)
    text = hansardReading.returnNormalised(text)
    return text    

def get_BOW(text):
    BOW = {}
    for word in text:
        if not word or word == ' ':
            continue
        BOW[word.lower()] = BOW.get(word.lower(),0) + 1
    return BOW


def convertFolders(folders, isNew):
    outputDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised/"
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    for folder in folders:
        input_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/{0}".format(folder) 

        for filename in os.listdir(input_directory):
            split = str(filename).split('.')
            extension = split[-1].lower()
            if extension != 'xml':
                continue
            date = split[0]
            fileLocation = input_directory+'/'+filename

            text = singleDocumentToNormalised(fileLocation, isNew).split(' ')
            bow = get_BOW(text)
            outputFileDirectory = outputDirectory+date+".json"
            outputFile = open(outputFileDirectory, 'w')
            json.dump(bow, outputFile)



oldFolders = [str(x) for x in range(1998,2011)] 
oldFolders.append('2011_before_april')
newFolders = [str(x) for x in range(2011,2018)] 

convertFolders(oldFolders, False)
convertFolders(newFolders, True)


#vectorizer = DictVectorizer()
#matrix = vectorizer.fit_transform([text]).transpose()

#print matrix