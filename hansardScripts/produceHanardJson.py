import readNewHansard
import readOldHansard
import os
import json
def BowToJson(folders, modu):


    outputDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/byParty/bowNotNormalised/"
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
            bow = modu.produceBowByParty(fileLocation)


            outputFileDirectory = outputDirectory+date+".json"
            outputFile = open(outputFileDirectory, 'w')
            json.dump(bow, outputFile)

oldFolders = [str(x) for x in range(1998,2011)] 
oldFolders.append('2011_before_april')
BowToJson(oldFolders, readOldHansard)


newFolders = [str(x) for x in range(2011,2018)] 
BowToJson(newFolders, readNewHansard)



