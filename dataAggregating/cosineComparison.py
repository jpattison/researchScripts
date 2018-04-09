"""
Sort of working. I think the names of people is throwing it off. We'll need to aggregate it by month or something for better.

"""


import json
from sklearn.feature_extraction import DictVectorizer
import os
from scipy.spatial.distance import cosine as cos_distance
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD



def createMatrix(folder):
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
    vectorizer = DictVectorizer()
    matrix = vectorizer.fit_transform(documents)
    return reference, matrix


def performTfidf(matrix):
  transformer = TfidfTransformer(smooth_idf=False,norm=None)
  return transformer.fit_transform(matrix)  

def svdTransform(matrix, k):
  svd = TruncatedSVD(n_components=k)  
  return svd.fit_transform(matrix)

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
    results.sort(key=lambda x: x[1])
    return results

folder = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bow/"
reference, matrix = createMatrix(folder)
print "perform transformations"
matrix = performTfidf(matrix)
matrix = svdTransform(matrix, 100) # k should be a lot higher

# 1225: '2014-12-04 
# 241: 2014-05-14
# budget 2014 2014-05-14

queryId = 0

for key in reference:
    if reference[key]=="2014-05-14":
        print "its {0}".format(key)
        queryId = key
        break

query = matrix[queryId] # note this wasn't done in assignment
#query.shape = (153479)
#print query

scores = scoreDocuments(query, matrix, reference)
print "final scores \n\n"
print scores

