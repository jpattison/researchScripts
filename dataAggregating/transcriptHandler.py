"""
Idea. If we want to pull specific  information about transcripts in a format similar to what hansard has

"""

import os
import json
from datetime import datetime

bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/budgetBOW"

budgetYear = {2005: {"start": 10, "end": 12}, 2006: {"start": 9, "end": 11}, 2007: {"start": 8, "end": 10},
2008: {"start": 13, "end": 15}, 2009: {"start": 11, "end": 13}, 2010: {"start": 8, "end": 10}, 2011: {"start": 10, "end": 12},
2012: {"start": 8, "end": 10}, 2013: {"start": 14, "end": 16}, 2014: {"start": 13, "end": 15}, 2015: {"start": 12, "end": 14}}

def assignCategory(tranDate, dayBuf):
    global budgetYear
    year = tranDate.year
    day = tranDate.day
    if not year in budgetYear:
        #print "{0} not in budgetYear".format(year)
        return "N/A"
    start = budgetYear[year]["start"]
    end = budgetYear[year]["end"]

    if (day + dayBuf) < start or (day - dayBuf) > end:
        return "N/A"
    if day<start:
        return "before"
    if day<=end:
        return "during"
    else:
        return "after"

def mergeDic(dicArray):
    #print dicArray
    output = {}
    for dic in dicArray:
        for key in dic:
            if not key in output:
                output[key] = dic[key]
            else:
                output[key] += dic[key]
    return output


def getTranscripts(initialYear, finalYear, queryYear, mediaTypes, justBudgets = False, budgetCategories =[], source=bowDirectory):

    # ideally we need to make an object of conditions that is passed for both query and reference.
    queryTranscripts = [] # the query.
    yearBreadth = finalYear - initialYear +1
    listofBowYears = [list() for i in range(yearBreadth)] # the datasert
    reference = {}

    for filename in os.listdir(source):
        filepath = source + "/" + filename
        file = open(filepath)
        transcriptDic = json.loads(file.readline())
        dateString = transcriptDic["data-release-date"]
        tranType = transcriptDic["data-release-type"]
        tranDate = datetime.strptime(dateString, '%d/%m/%Y')
        year = tranDate.year
        day = tranDate.day

        if mediaTypes and not tranType in mediaTypes:
            
            continue

        if justBudgets:

            category = assignCategory(tranDate, 4)

            if category == "N/A":
                continue
            if budgetCategories and not category in budgetCategories:
                
                continue

        if year == queryYear:
            queryTranscripts.append(transcriptDic["BOW"])
        
        if year <= finalYear and year >= initialYear:
            pos = year - initialYear

            listofBowYears[pos].append(transcriptDic["BOW"])
            reference[pos]=year

    dataset = []
    for budgetYear in listofBowYears:
        dataset.append(mergeDic(budgetYear))

    queryTranscript = mergeDic(queryTranscripts)
    
    # want to remove the queryData from the dataset
    if queryYear <= finalYear and queryYear >= initialYear:
        pos = queryYear - initialYear
        dataset.pop(pos)
        for year in range(queryYear,finalYear):
            reference[pos] = reference[pos+1]
            pos = pos+1
        reference.pop(pos)

    return queryTranscript, dataset, reference

def splitByCategory(initialYear, finalYear, mediaTypes, dayBuff=4, source=bowDirectory):
    # dictionary of dictionary. Year => Category = BOW
    #yearBreadth = finalYear - initialYear +1
    bowYears = {} # for each key (year) is list list of raw bow

    for filename in os.listdir(source):
        filepath = source + "/" + filename
        file = open(filepath)
        transcriptDic = json.loads(file.readline())
        dateString = transcriptDic["data-release-date"]
        tranType = transcriptDic["data-release-type"]
        tranDate = datetime.strptime(dateString, '%d/%m/%Y')
        year = tranDate.year
        day = tranDate.day

        if mediaTypes and not tranType in mediaTypes:
            continue
        if year>finalYear or year <initialYear:
            continue
        category = assignCategory(tranDate, dayBuff)
        if category=="N/A":
            continue
        # at this point we assume data is valid

        if not year in bowYears:
            bowYears[year] = {}
        if not category in bowYears[year]:
            bowYears[year][category] = []      
        bowYears[year][category].append(transcriptDic["BOW"])

        #print transcriptDic["BOW"]
        #bowYears[year].append(transcriptDic["BOW"])

    dataset = {}
    #print bowYears[2010].keys()
    
    for year in bowYears:
        dataset[year]={}
        for category in bowYears[year]:
            dataset[year][category] = mergeDic(bowYears[year][category])

    return dataset




