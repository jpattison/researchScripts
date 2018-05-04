import os
import json
from datetime import datetime
import cosineComparison
import graphs
import transcriptHandler

"""
If I'm doing a call on the transcripts. It should be called from here

"""

bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/budgetBOW"


def checkDistribution():
### This code is for checking distributions of the data for specific categories

    # for 2005-2015 large change in distributions between years, within a year (before/during/after)
    # most of time it was sorta balanced

    dateMap ={}
    tranYearType = {}
    for filename in os.listdir(bowDirectory):
        filepath = bowDirectory + "/" + filename
        file = open(filepath)
        transcriptDic = json.loads(file.readline())
        dateString = transcriptDic["data-release-date"]
        tranType = transcriptDic["data-release-type"]
        tranDate = datetime.strptime(dateString, '%d/%m/%Y')
        year = tranDate.year
        day = tranDate.day
        category = transcriptHandler.assignCategory(tranDate, 4)
        if category =="N/A":
            continue

        if not year in dateMap:
            dateMap[year]= {}
            tranYearType[year] = {}


        if not category in dateMap[year]:
            dateMap[year][category] = 0

        if not category in tranYearType[year]:
            tranYearType[year][category] = {}


        if not tranType in tranYearType[year][category]:
            tranYearType[year][category][tranType]=0

        dateMap[year][category] +=1
        tranYearType[year][category][tranType] += 1

    for year in dateMap:
        print year
        for category in dateMap[year]:
            print "\t{0}:{1}".format(category, dateMap[year][category])
    print "\n\n\n"
    for year in tranYearType:
        print year
        for category in tranYearType[year]:
            print category
            print tranYearType[year][category]


def compareDivergence(referenceYear, queryYear):
    
    referenceBudget =[] # the specific year we care about
    queryBudget = []

    for filename in os.listdir(bowDirectory):
        filepath = bowDirectory + "/" + filename
        file = open(filepath)
        transcriptDic = json.loads(file.readline())
        dateString = transcriptDic["data-release-date"]
        tranType = transcriptDic["data-release-type"]
        tranDate = datetime.strptime(dateString, '%d/%m/%Y')
        year = tranDate.year
        day = tranDate.day
        category = assignCategory(tranDate, 4)
        
        if category =="N/A" or (tranType!="Media Release" and tranType!="Speech" and tranType!="Transcript"):
            continue

        if year == referenceYear:
            referenceBudget.append(transcriptDic["BOW"])
        elif year == queryYear:
            queryBudget.append(transcriptDic["BOW"])
        else:
            continue

    pBow  = mergeDic(referenceBudget)
    qBow = mergeDic(queryBudget)
    klWords, missing = cosineComparison.KLdivergenceWords(pBow, qBow)

    klWords = klWords.items()

    klWords.sort(key=lambda x: x[1])


    for wordPair in klWords[-100:]:
        word = wordPair[0]
        print("Word: {0} 2005: {1} 2014: {2}".format(word, pBow[word], qBow[word]))


def KlPmTranscripts(dataset, queryTranscript, queryName, reference):

    #print dataset
    matrix, query = cosineComparison.matrixQueryNoTransformation(dataset, queryTranscript)

    #print(matrix)
    scores = cosineComparison.inverseKLdivergence(query, matrix, reference) #jointEntropy
    scores.sort(key=lambda x: x[0])

    print scores

    xAxis = [pair[0] for pair in scores]
    values = [pair[1] for pair in scores]
    graphs.makeGraph(xAxis, "scores", "transcript budget log for {0}".format(queryName), values, queryName)




def cosineTranscripts(dataset, queryTranscript, queryName, reference, k):
    matrix, query = cosineComparison.calculateComparison(dataset, queryTranscript, k)
    scores = cosineComparison.scoreDocuments(query, matrix, reference)

    xAxis = [pair[0] for pair in scores]
    values = [pair[1] for pair in scores]
    graphs.makeGraph(xAxis, "scores", "Transcript Cosine. Reference = {0} K = {1}".\
        format(queryName,k), values)

# This does the languaguage analysis based on cosine method

# k = 100
# reference, documents = cosineComparison.arrayToBow(budgets, bowDirectory)
# _, queryBow = cosineComparison.arrayToBow([referenceBudget], bowDirectory)
# #matrix, query = cosineComparison.calculateComparison(documents, queryBow, k)
# matrix, query = cosineComparison.matrixQueryNoTransformation(documents, queryBow[0])

# #scores = cosineComparison.scoreDocuments(query, matrix, reference) # cosine
# scores = cosineComparison.inverseKLdivergence(query, matrix, reference) #jointEntropy

# xAxis = [pair[0][0:4] for pair in scores]
# values = [pair[1] for pair in scores]
# print scores


# graphs.makeGraph(xAxis, "scores", "budget comparison. Reference = 2006", values)

queryTranscript, dataset, reference = \
    transcriptHandler.getTranscripts(2005, 2015, 2014, None, True, ["after"])

#KlPmTranscripts(dataset, queryTranscript, "2015", reference)
cosineTranscripts(dataset, queryTranscript, "2014", reference, 1000)


