import readNewHansard
import readOldHansard
import os
import json
def BowToJson(folders, modu, removeCapitals, stemWords):


    outputDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/byParty/bowNormalisedNotStemmed/"
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

            print fileLocation
            bow = modu.produceBowByParty(fileLocation, removeCapitals, stemWords)


            outputFileDirectory = outputDirectory+date+".json"
            outputFile = open(outputFileDirectory, 'w')
            json.dump(bow, outputFile)


removeCapitals = True 
stemWords = False

oldFolders = [str(x) for x in range(1998,2011)] 
oldFolders.append('2011_before_april')
BowToJson(oldFolders, readOldHansard, removeCapitals, stemWords)


newFolders = [str(x) for x in range(2011,2018)] 
BowToJson(newFolders, readNewHansard, removeCapitals, stemWords)



