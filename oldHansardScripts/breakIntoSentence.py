# suppose we want to output json of documents broken by sentence we do that here
# main thing is that the output will be a single json file per hansardFile with list of represneations (be it bow of words or whatever)

import sys
import hansardReading
import xml.etree.ElementTree as ET
import nltk
import os
import json
#sys.path.insert(0, '/path/to/application/app/folder')

#outputDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/sentenceNoProperNouns/"


outputDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/sentenceNoProperNouns/"

def removeProperNouns(root, isNew):
    # removes words starting with capital letters or punctuation
    # note the Boolean decides if we're removing stop words as well
    output = []
    if isNew:
        sentences = hansardReading.updatedReadNewText(root, False)
    else:
        sentences = hansardReading.updatedReadOldText(root, False)

    for sentence in sentences:
        output.append(" ".join(sentence))

    return output


def justSentences(root, isNew):
    # Produces a list of 
    if isNew:
        return hansardReading.newToSentences(root)
    else:
        return hansardReading.oldToSentences(root)

def methodToJson(folders, isNew, methodToRun):
    global outputDirectory
    #outputDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/sentenceNoProperNouns/"
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

            file = open(fileLocation)
            tree = ET.parse(file)
            root = tree.getroot()

            text = methodToRun(root, isNew)
            # if isNew:
            #     #text = hansardReading.newToSentences(root)
            #     text = newMethodToRun(root)
            # else:
            #     #text = hansardReading.oldToSentences(root)
            #     text = oldMethodToRun(root)

            outputFileDirectory = outputDirectory+date+".json"
            outputFile = open(outputFileDirectory, 'w')
            json.dump(text, outputFile)







oldFolders = [str(x) for x in range(1998,2011)] 
oldFolders.append('2011_before_april')
newFolders = [str(x) for x in range(2011,2018)] 


# we want to keep "semipure sentences"
methodToJson(oldFolders, False, removeProperNouns)
methodToJson(newFolders, True, removeProperNouns)




