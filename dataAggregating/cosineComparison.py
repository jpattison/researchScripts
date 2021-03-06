"""
Sort of working. I think the names of people is throwing it off. We'll need to aggregate it by month or something for better.

"""


import json
from sklearn.feature_extraction import DictVectorizer
import os
from scipy.spatial.distance import cosine as cos_distance
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from datetime import datetime
import numpy as np
import graphs
import math
import copy

# def folderToBow(folder):
#     reference = {} 
#     i = 0
#     documents = []
#     for filename in os.listdir(folder):
#         split = str(filename).split('.')
#         extension = split[-1].lower()
#         date = split[0]
#         if extension != 'json':
#             continue

#         filePath = folder+'/'+filename
#         inputFile = open(filePath)
#         bow = json.loads(inputFile.readline())
#         documents.append(bow)
#         reference[i]=date
#         i +=1
#     return reference, documents
#     vectorizer = DictVectorizer()
#     matrix = vectorizer.fit_transform(documents)
#     return reference, matrix, vectorizer

# def arrayToBow(docArray, folder=None):
#     # same as folderToBow but assumes a list of lists for documents
#     # if multiple documents in same inner list then merge. But like by putting individual we can easily just use as a singular as well
#     documents = []
#     i = 0
#     reference = {}
#     for docSet in docArray:
#         doc = {}
#         name = None
#         for filename in docSet:
#             if name == None:
#                 name = filename
#                 reference[i]=name
#                 i+=1
#             if folder:
#                 tempFile = open(folder+filename)
#             else:
#                 tempFile = open(filename)
            
#             bow = json.loads(tempFile.readline())

#             for key in bow:
#                 if key in doc:
#                     doc[key] += bow[key]
#                 else:
#                     doc[key] = bow[key]
#         documents.append(doc)
#     return reference, documents



# def fileToBow(fileLocation):
#     file = open(fileLocation)
#     bow = json.loads(file.readline())
#     return bow

# def performTfidf(matrix):
#   transformer = TfidfTransformer(smooth_idf=False,norm=None)
#   return transformer.fit_transform(matrix)  

# def svdTransform(matrix, k):
#   svd = TruncatedSVD(n_components=k)  
#   return svd.fit_transform(matrix)

def scoreDocuments(query, matrix, reference):
    results = [] #(reference, score)

    i = 0

    for column in matrix:
        # print query.shape
        # print matrix[i].shape
        # print matrix[i]

        score = cos_distance(query, matrix[i])
        name = reference[i]
        results.append([name, score])
        i = i+1
        # if i%100 == 0:
        #     print matrix[i]
        #     print score
    #print results
    #results.sort(key=lambda x: x[1])
    return results

def KLdivergence(query, matrix, reference, smoothing):
    # https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence

    results = []
    count = 0

    #print matrix

    #print len(matrix)
    for column in matrix:
        # summation = 0.0
        # length = len(column)
        # sumCompared = sum(column)
        # for i in range(0,len(column)):
        #     qBow = query[i]*1.0 / sumQuery #Q
        #     pBow = column[i]*1.0 / sumCompared #P
        #     #tProb = qBow * pBow
        #     if qBow ==0 or pBow ==0:
        #         continue
        #     #print tProb
        #     #print query[i]
        #     #print column[i]
        #     summation -= pBow * math.log(qBow/pBow,2) 
        # #summation += 1 # avoiding the log0 error
        


        name = reference[count]
        count+=1
        #print name
        results.append([name, KLbow(column, query, smoothing)])

    #results.sort(key=lambda x: x[1])
    return results

def KLBackwardsDivergence(query, matrix, reference, smoothing):
    """
    Have the matrix as the reference and predict query

    """
    results = []
    count = 0

    for column in matrix:
        name = reference[count]
        count+=1
        results.append([name, KLbow(query, column, smoothing)])     
    return results   



def calcSumBow(bow):
    # return the total number of words
    total = 0
    for key in bow:
        total += bow[key]
    return total


def KLbow(pBow, qBow, plusOneSmoothing):
    # https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence
    # KL estimates the distribution difference. D(P|Q). Q DOES NOT stand for query, instead it is our base.


    if plusOneSmoothing:
        print "note you're smoothing"
        qBow = copy.deepcopy(qBow)
        qBow = plusOneSmooth(qBow, pBow)
    denP = calcSumBow(pBow) # denominator for P
    denQ = calcSumBow(qBow) # denominator for Q


    KL = 0.0

    for word in pBow:
        probP = pBow[word]*1.0/denP
        if word not in qBow:
            #print "skipped a number"
            continue # we give it a value of 0 but this probably isn't a good assumption
        probQ = qBow[word]*1.0/denQ
        kInstance = probP * math.log(probP/probQ,2)
        KL += kInstance
    return KL



"""
def cosineBOW(queryBow, dataBow):
    # two bag of words.
    #Just do cosine comparison, no TFIDF or anything
    #matrix, query = calculateComparison(bowReference, bowQuery, None)
    
    vectorizer = DictVectorizer()
    
    data = vectorizer.fit_transform(dataBow).toarray()
    query = vectorizer.transform(queryBow).toarray()

    # print data
    # print "inbetween2 \n"
    # print query
    return cos_distance(query, data)
"""
def KLdivergenceWords(qBow, pBow):

    # KL estimates the distribution difference. D(Q|P). Find contribution by word


    words = {} #kl for each word in pBow
    missing = {} # counts of words that are in qBow but not pBow. Not as useful
    pLen = 0
    qLen = 0
    for word in qBow:
        words[word] = 0
        qLen += qBow[word]
    pKeys = pBow.keys()

    for word in pBow:
        pLen += pBow[word]

    for word in qBow:
        if not word in pBow:
            missing[word] = qBow[word]
            continue
        pProb = pBow[word] * 1.0 / pLen
        qProb = qBow[word] * 1.0 / qLen

        words[word] = pProb * math.log(pProb/qProb,2)

    return words, missing

def plusOneSmooth(base, p):
    ### want to do plus one smoothing add an instance of p to base to ensure nothing is skipped
    

    for word in p:
        if not word in base:
            base[word]=1
    return base






def transform_query(svd, transformer, query, vectorizer):
    queryMatrix = svd.transform(transformer.transform(vectorizer.transform(query)))
    return queryMatrix[0]

def calculateComparison(bowReference, bowQuery, k):
    vectorizer = DictVectorizer()
    matrix = vectorizer.fit_transform(bowReference)
    

    transformer = TfidfTransformer(smooth_idf=False,norm=None)

    matrix = transformer.fit_transform(matrix) 

    if k:
        svd = TruncatedSVD(n_components=k)
        matrix = svd.fit_transform(matrix)
        query = transform_query(svd, transformer, bowQuery, vectorizer)
    else:
        matrix = matrix.toarray()
        query = transformer.transform(vectorizer.transform(bowQuery)).toarray()[0]
    # print "query"
    # print len(query)
    # print "matrix"
    # print len(matrix)

    return matrix, query

def matrixQueryNoTransformation(bowReference, bowQuery):
    # pretty much identicle to calculateComparison but no bs with transformations.
    
    # note we add a cell for 'other'. I'm not sure if this is the correct way tbh

    # print bowReference
    # print len(bowReference)
    keys = bowQuery.keys()

    matrix = []

    for ref in bowReference:
        bowList = []
        for key in keys:
            if key in ref:
                bowList.append(ref[key])
            else:
                bowList.append(0)
        noneValue = 0 #dump all words that didn't appear in query here
        for key in ref:
            if not key in keys:
                noneValue += ref[key]
        bowList.append(noneValue)
        matrix.append(bowList)

    query = []

    for key in keys:
        query.append(bowQuery[key])

    query.append(0) # blank for others
    return matrix, query



def cosineToDicForm(scores):
    dicForm = {}
    for dateString, score in scores:
        date = datetime.strptime(dateString, '%Y-%m-%d')
        dicForm[date] = score
    return dicForm

def generateMonths():
    return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def graphByMonthGraph(dicForm, title, context):
    monthScore = np.ones([12]).tolist() # value is on dissimilarity so start at one
    months = generateMonths()
    
    for date in dicForm:

        month = date.month -1
        monthScore[month]-=dicForm[date] # subtract dissimilarlity
    graphs.makeGraph(months, "accumulative scores", title, monthScore, context)

def calculateMinMaxYear(dates):
    maxYear = minYear = dates[0].year

    for date in dates:
        maxYear = max(maxYear, date.year)
        minYear = min(minYear, date.year)
    return maxYear, minYear


def graphByMonthYearGraph(dicForm, title, context):
    maxYear, minYear = calculateMinMaxYear(dicForm.keys())
    numYears = maxYear - minYear + 1
    print maxYear 
    print minYear 
    print numYears
    monthScore = np.ones([12*(numYears)]).tolist()

    print "len is {0}".format(len (monthScore))
    xLabel = numYears * generateMonths()
    for date in dicForm:
        #print date
        yearOffset = date.year - minYear
        monthOffset = date.month - 1
        indexOffset = yearOffset * 12 + monthOffset

        monthScore[indexOffset] += ( 1 - dicForm[date]) # attempt to make high look good. Note we need to normalise by number in that month

    graphs.makeGraph(xLabel, "accumulative scores", title, monthScore, context)
 


def calculateSingleReference(bowDirectory, queryLocation, k):
    reference, bowCorpus= folderToBow(bowDirectory)
    queryBow = fileToBow(queryLocation)
    
    matrix, query = calculateComparison(bowCorpus, queryBow, k)
    
    return scoreDocuments(query, matrix, reference)


def scoreMultipleReferenceDic(bowDirectory, queryFiles, k):
    # takes in mulitple query files and creates a dictionary of similarity
    reference, bowCorpus= folderToBow(bowDirectory)

    dicSolution = {}

    for queryFile in queryFiles:
        queryBow = fileToBow(queryFile)

        matrix, query = calculateComparison(bowCorpus, queryBow, k)

        tempScore = scoreDocuments(query, matrix, reference)

        for dateString, score in tempScore:
            date = datetime.strptime(dateString, '%Y-%m-%d')
            if date in dicSolution:
                dicSolution[date] += score
            else:
                dicSolution[date] = score

    return dicSolution



def dicScoreToSortedList(dicScore):
    output = []
    for key in dicScore:
        output.append([key, dicScore[key]])

    output.sort(key=lambda x: x[1])

    return output


#def calculateByMonthYear(bowDirectory, stringMonth):

#bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bow/"





# given we aren't getting perfect 0 for 14th, i thnk slightly off