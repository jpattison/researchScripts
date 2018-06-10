import os
import json
from datetime import datetime
import cosineComparison
import graphs
import transcriptHandler

"""
If I'm doing a call on the transcripts. It should be called from here

"""

bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/bowNormalisedStemmed"




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
    scores = cosineComparison.KLdivergence(query, matrix, reference) #jointEntropy
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


def KlWithinYear(initialYear, finalYear, mediaTypes = None, dayBuff = 4):
    # returns a list of lists + reference
    # query is before budget. First value is KL during, second is after
    splitBy = transcriptHandler.splitByCategory(initialYear, finalYear, mediaTypes, dayBuff)
    results = []
    years = []
    keys = []
    for year in sorted(splitBy.keys()):
        key = []
        key.append("during")
        key.append("after")
        key.append("duringVafter")

        if not "before" in splitBy[year]:
            print("Error: no before to base off. Deal with")
            print year
        years.append(str(year))
        #print splitBy[year]["during"]
        before = splitBy[year]["before"]
        during = splitBy[year]["during"]
        after = splitBy[year]["after"]
        # before = transcriptHandler.mergeDic(beforeSet)
        # during = transcriptHandler.mergeDic(duringSet)
        # after = transcriptHandler.mergeDic(afterSet)

        duringKL = cosineComparison.KLbow(before, during)
        afterKL = cosineComparison.KLbow(before, after)
        duringAfter = cosineComparison.KLbow(during, after)

        results.append([duringKL, afterKL, duringAfter])
        keys.append(key)
    return results, years, keys


def cosineWithinYear(initialYear, finalYear, mediaTypes = None, dayBuff = 4):
    # returns a list of lists + reference
    # query is before budget. First value is KL during, second is after
    splitBy = transcriptHandler.splitByCategory(initialYear, finalYear, mediaTypes, dayBuff)
    results = []
    years = []
    keys = []
    for year in sorted(splitBy.keys()):
        key = []
        key.append("during")
        key.append("after")
        key.append("duringVafter")
        if not "before" in splitBy[year]:
            print("Error: no before to base off. Deal with")
            print year
        years.append(str(year))
        #print splitBy[year]["during"]
        before = splitBy[year]["before"]
        during = splitBy[year]["during"]
        after = splitBy[year]["after"]
        # before = transcriptHandler.mergeDic(beforeSet)
        # during = transcriptHandler.mergeDic(duringSet)
        # after = transcriptHandler.mergeDic(afterSet)

        duringCo = cosineComparison.cosineBOW(before, during)
        afterCo = cosineComparison.cosineBOW(before, after)
        duringAfter = cosineComparison.cosineBOW(during, after)
        results.append([duringCo, afterCo, duringAfter])

        keys.append(key)
    #print keys
    return results, years, keys



#2005To2009

refYear = 2013
queryTranscript, dataset, reference = \
    transcriptHandler.getTranscriptsBudgetDateTechnique(2010, 2014, refYear, None, bowDirectory, False, False, True)


print queryTranscript
print dataset
print reference

KlPmTranscripts(dataset, queryTranscript, str(refYear), reference)
#cosineTranscripts(dataset, queryTranscript, str(refYear), reference, None)

#2005, 2006, 2007, 2008, 2010, 2013, 2014, 2015, 2016, 2017

#results, years, keys= KlWithinYear(2005, 2015)
#results, years, keys= cosineWithinYear(2010, 2015)

# print results
#print results
#graphs.setSubplots(keys, years, "KL Before", results )


#cosine2010To2015

