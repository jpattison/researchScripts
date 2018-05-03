# same functionality as bagOfWords in hansard scripts with a lot of it ripped off

# idea is to give it two years and it will print bag of words for all in between
import json

import readTranscript
import os

SPEECHLOCATION = "/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/2003to2015"

output_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/budgetBOW"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


def paraToBow(sentences):   
    # assumes sentences (list of list)

    BOW = {}

    for sentence in sentences:
        for word in sentence:
            if not word in BOW:
                BOW[word] = 0
            BOW[word] += 1
    return BOW



for filename in os.listdir(SPEECHLOCATION):
    fileMap = {}
    split = str(filename).split('.')

    if len(split) > 1 : # i.e. has a file extension
        #print split
        continue

    file_path = SPEECHLOCATION+'/'+filename

    transcriptDic = readTranscript.transcriptToDic(file_path)
    if transcriptDic["data-release-date"].month!=5:
        continue
    transcriptDic = readTranscript.normaliseTranscript(transcriptDic)

    transcriptDic["BOW"] = paraToBow(transcriptDic["normalised"])

    #print transcriptDic["BOW"]

    output_path = output_directory+'/'+filename+'.json'
    outputFile = open(output_path, 'w')

    #datetime not serilizable so need to put into string
    transcriptDic["data-release-date"] = transcriptDic["data-release-date"].strftime("%d/%m/%Y")
    json.dump(transcriptDic, outputFile)

