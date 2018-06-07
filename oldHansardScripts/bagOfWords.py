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
    # first attempt in returning normalised page.
    # NOTE OUTDATED
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

def getNormalisedDocument(fileLocation, isNew):
    # normalise document and return list of sentences having gone normalisation
    # got rid of stop words + got rid of capitalised words (apart from first)
    input_file = open(fileLocation)
    tree = ET.parse(input_file)
    
    if isNew:
        sentences = hansardReading.updatedReadNewText(tree.getroot())
    else:
        sentences = hansardReading.updatedReadOldText(tree.getroot())    
    return sentences

def get_BOW(text):
    #assumes a list of words
    BOW = {}
    for word in text:
        if not word or word == ' ':
            continue
        BOW[word.lower()] = BOW.get(word.lower(),0) + 1
    return BOW

def paraToBow(sentences):   
    # assumes sentences (list of list)

    BOW = {}

    for sentence in sentences:
        for word in sentence:

            if not word in BOW:
                BOW[word] = 0
            BOW[word] += 1
    return BOW


# def convertFolders(folders, isNew):
#     outputDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised/"
#     if not os.path.exists(outputDirectory):
#         os.makedirs(outputDirectory)

#     for folder in folders:
#         input_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/{0}".format(folder) 

#         for filename in os.listdir(input_directory):
#             split = str(filename).split('.')
#             extension = split[-1].lower()
#             if extension != 'xml':
#                 continue
#             date = split[0]
#             fileLocation = input_directory+'/'+filename

#             text = singleDocumentToNormalised(fileLocation, isNew).split(' ')
#             bow = get_BOW(text)
#             outputFileDirectory = outputDirectory+date+".json"
#             outputFile = open(outputFileDirectory, 'w')
#             json.dump(bow, outputFile)

def compareBOW(folders, isNew):
    # This is to compare the old method with new method. At the moment we're getting quite different results
    # although I can't determine the actual causations
    # Morphology related stuff in the old method will play a part but that can't be all
    # also cucko was more aggressive in stop words

    for folder in folders:
        input_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/{0}".format(folder) 

        for filename in os.listdir(input_directory):
            split = str(filename).split('.')
            extension = split[-1].lower()
            if extension != 'xml':
                continue
            date = split[0]
            fileLocation = input_directory+'/'+filename

            text = getNormalisedDocument(fileLocation, isNew)
            bow = paraToBow(text)

            oldText = singleDocumentToNormalised(fileLocation, isNew).split(' ')
            oldBow = get_BOW(oldText)

            print "\n\n\n"+filename

            for key in bow:
                if not key in oldBow:
                    oldNum = 0
                else:
                    oldNum = oldBow[key]
                num = bow[key]
                if num != oldNum:
                    # print str(num) == str(oldNum)
                    # print num != oldNum
                    # print type(num)
                    # print type(oldNum)
                    print("{0}: New: {1} Old: {2}".format(key, num, oldNum))
            break

            # outputFileDirectory = outputDirectory+date+".json"
            # outputFile = open(outputFileDirectory, 'w')
            # json.dump(bow, outputFile)

def convertFolders(folders, isNew):
    outputDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised2/"
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

            text = getNormalisedDocument(fileLocation, isNew)
            bow = paraToBow(text)


            outputFileDirectory = outputDirectory+date+".json"
            outputFile = open(outputFileDirectory, 'w')
            json.dump(bow, outputFile)


def convertStemmedFolders(folders, isNew):
    outputDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalisedStemmed/"
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

            text = getNormalisedDocument(fileLocation, isNew)
            # print "\n\nInitial"
            # print text[0:10]
            text = hansardReading.stemParagraph(text)
            # print "\n\nStemmed"
            # print text[0:10]
            # print"\n\nBow"
            bow = paraToBow(text)
            #print(bow)
            #return
            outputFileDirectory = outputDirectory+date+".json"
            outputFile = open(outputFileDirectory, 'w')
            json.dump(bow, outputFile)


oldFolders = [str(x) for x in range(1998,2011)] 
oldFolders.append('2011_before_april')
newFolders = [str(x) for x in range(2011,2018)] 


# convertFolders(newFolders, True)
# convertFolders(oldFolders, False)

convertStemmedFolders(newFolders, True)
convertStemmedFolders(oldFolders, False)

#vectorizer = DictVectorizer()
#matrix = vectorizer.fit_transform([text]).transpose()

#print matrix