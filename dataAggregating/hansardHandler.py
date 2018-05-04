"""
Idea I want to pull out a specific set of hansard documents.

Output should generally be bag of words of corpus, query and a reference

"""

bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised2/"


import json

import os

budget2017 = ["2017-05-09.json","2017-05-10.json","2017-05-11.json"]

budget2016 = ["2016-05-02.json", "2016-05-03.json", "2016-05-04.json", "2016-05-05.json"]

budget2015 = ["2015-05-12.json","2015-05-13.json","2015-05-14.json"]

budget2014 = ["2014-05-13.json","2014-05-14.json","2014-05-15.json"]

budget2013 = ["2013-05-14.json","2013-05-15.json","2013-05-16.json"]

budget2012 = ["2012-05-08.json", "2012-05-09.json", "2012-05-10.json"]

budget2011 = ["2011-05-10.json", "2011-05-11.json", "2011-05-10.json", "2011-05-12.json"]

budget2010 = ["2010-05-11.json", "2010-05-12.json", "2010-05-13.json"]

budget2009 = ["2009-05-12.json", "2009-05-13.json", "2009-05-14.json"]

budget2008 = ["2008-05-13.json", "2008-05-14.json", "2008-05-15.json"]

budget2007 = ["2007-05-08.json", "2007-05-09.json", "2007-05-10.json"]

budget2006 = ["2006-05-09.json", "2006-05-10.json", "2006-05-11.json"]

budget2005 = ["2005-05-10.json", "2005-05-11.json", "2005-05-12.json"]

"""
budgetList = [(budget2005, "budget2005"), (budget2006, "budget2006 Howard Last"), 
(budget2007, "budget2007 Rudd First"), (budget2008, "budget2008"), (budget2011, "budget2011 Gillard first"), (budget2013, "budget2013 gillard last"),
(budget2014, "budget2014"), (budget2017, "budget2017")]
"""

budgetList = [(budget2005, 2005), (budget2006, 2006), 
(budget2007, 2007), (budget2008, 2008), (budget2009, 2009),
(budget2010, 2010), (budget2011, 2011), (budget2013, 2013),
(budget2014, 2014), (budget2015, 2015), (budget2016, 2016),
(budget2017, 2017)]

# I suppose the basic would be convert an entire year into single bag of words and use that
#def getHansard(initialYear, finalYear, queryYear, source=bowDirectory)


# only cares about the budgets
def getHansardBudgets(initialYear, finalYear, queryYear, source=bowDirectory):
    years = [el[1] for el in budgetList]
    yearPos = years.index(queryYear)
    queryList = budgetList[yearPos][0]
    print queryList

    budgetList.pop(yearPos)

    budgetReduced = [] # ones within specific years
    for pair in budgetList:
        year = pair[1]
        if year <= finalYear and year >= initialYear and year != queryYear:
            budgetReduced.append(pair[0])
    reference, dataset = arrayToBow(budgetReduced, source)
    _, queryTranscript = arrayToBow([queryList], source)
    queryTranscript = queryTranscript[0]

    return queryTranscript, dataset, reference 


def folderToBow(folder):
    reference = {} 
    i = 0
    documents = []
    for filename in os.listdir(folder):
        split = str(filename).split('.')
        extension = split[-1].lower()
        date = split[0]
        if extension != 'json':
            continue

        filePath = folder+'/'+filename
        inputFile = open(filePath)
        bow = json.loads(inputFile.readline())
        documents.append(bow)
        reference[i]=date
        i +=1
    return reference, documents
    vectorizer = DictVectorizer()
    matrix = vectorizer.fit_transform(documents)
    return reference, matrix, vectorizer

def arrayToBow(docArray, folder=None):
    # same as folderToBow but assumes a list of lists for documents
    # if multiple documents in same inner list then merge. But like by putting individual we can easily just use as a singular as well
    documents = []
    i = 0
    reference = {}
    for docSet in docArray:
        doc = {}
        name = None
        for filename in docSet:
            if name == None:
                name = filename
                reference[i]=int(name[:4])
                i+=1
            if folder:
                tempFile = open(folder+filename)
            else:
                tempFile = open(filename)
            
            bow = json.loads(tempFile.readline())

            for key in bow:
                if key in doc:
                    doc[key] += bow[key]
                else:
                    doc[key] = bow[key]
        documents.append(doc)
    return reference, documents

def fileToBow(fileLocation):
    file = open(fileLocation)
    bow = json.loads(file.readline())
    return bo

