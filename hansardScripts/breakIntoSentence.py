import sys
import hansardReading
import xml.etree.ElementTree as ET
import nltk
import os
import json
#sys.path.insert(0, '/path/to/application/app/folder')





def grabSentences(folders, isNew):
    outputDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/sentences/"
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

            if isNew:
                text = hansardReading.newToSentences(root)
            else:
                text = hansardReading.oldToSentences(root)

            outputFileDirectory = outputDirectory+date+".json"
            outputFile = open(outputFileDirectory, 'w')
            json.dump(text, outputFile)


oldFolders = [str(x) for x in range(1998,2011)] 
oldFolders.append('2011_before_april')
newFolders = [str(x) for x in range(2011,2018)] 

grabSentences(oldFolders, False)
grabSentences(newFolders, True)