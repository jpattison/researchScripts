import hansardHandler
import cosineComparison
import graphs

bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalisedStemmed/"


def cosineHansard(dataset, queryTranscript, queryName, reference, k):
    matrix, query = cosineComparison.calculateComparison(dataset, queryTranscript, k)
    scores = cosineComparison.scoreDocuments(query, matrix, reference)

    xAxis = [pair[0] for pair in scores]
    values = [pair[1] for pair in scores]
    graphs.makeGraph(xAxis, "scores", "Hansard Cosine. Reference = {0} K = {1}".\
        format(queryName,k), values)



def KlHansard(dataset, queryTranscript, queryName, reference):

    #print dataset
    matrix, query = cosineComparison.matrixQueryNoTransformation(dataset, queryTranscript)

    #print(matrix)
    scores = cosineComparison.KLdivergence(query, matrix, reference) #jointEntropy
    scores.sort(key=lambda x: x[0])

    print scores

    xAxis = [pair[0] for pair in scores]
    values = [pair[1] for pair in scores]
    graphs.makeGraph(xAxis, "scores", "Hansard for {0}".format(queryName), values, queryName)

queryYear = 2017

#2005, 2006, 2007, 2008, 2010, 2013, 2014, 2015, 2016, 2017
# note leaving k = None means to svd transform :( 

queryTranscript, dataset, reference = \
   hansardHandler.budgetToBow(2005, 2017, queryYear, False, True, False, bowDirectory)
#def budgetToBow(initialYear, finalYear, queryYear, budgetSession = False, budgetEstimates = False, skipFirstDay = False, source=bowDirectory)


#print len(dataset)
print reference
#cosineHansard(dataset, queryTranscript, str(queryYear), reference, None)

KlHansard(dataset, queryTranscript, str(queryYear), reference)


