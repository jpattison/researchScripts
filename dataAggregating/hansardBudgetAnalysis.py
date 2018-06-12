import hansardHandler
import cosineComparison
import graphs

#bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalisedStemmed/"
# bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/byParty/bowNormalisedAndStemmed/"

bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/byParty/bowNotNormalised/"


"""
def cosineHansard(dataset, queryTranscript, queryName, reference, k):
    matrix, query = cosineComparison.calculateComparison(dataset, queryTranscript, k)
    scores = cosineComparison.scoreDocuments(query, matrix, reference)

    xAxis = [pair[0] for pair in scores]
    values = [pair[1] for pair in scores]
    graphs.makeGraph(xAxis, "scores", "Hansard Cosine. Reference = {0} K = {1}".\
        format(queryName,k), values)
"""


def KlHansard(dataset, queryTranscript, queryName, reference):
    # This is for when i have a specific target year to compare others to
    #print dataset

    #print(matrix)
    scores = cosineComparison.KLdivergence(queryTranscript, dataset, reference) #jointEntropy

    print scores


    xAxis = [pair[0] for pair in scores]
    values = [pair[1] for pair in scores]
    graphs.makeGraph(xAxis, "scores", "KL Hansard for {0}".format(queryName), values, queryName)


def KlHansardIterative(dataset, reference):
    # I want to compare the previous year to current year itteratively
    print reference
    print len(dataset)  
    #print dataset[0]
    klValues = []
    yearsInvestigated = []
    for i in range(1,len(dataset)):
        priorBow = dataset[i-1]
        currentBow = dataset[i]
        currentYear = reference[i]
        
        yearsInvestigated.append(currentYear)
        klValues.append(cosineComparison.KLbow(currentBow, priorBow))

    print klValues
    graphs.makeGraph(yearsInvestigated, "scores", "KL Government", klValues, "not sure what this is")





partyFunction = hansardHandler.filenameToPartyInCharge #fileNameToOppsition #filenameToPartyInCharge




queryYear = 2006

# queryTranscript, dataset, reference = \
#    hansardHandler.budgetToBow(2005, 2017, queryYear, partyFunction, False, True, False, bowDirectory)

"""

print reference
#cosineHansard(dataset, queryTranscript, str(queryYear), reference, None)
KlHansard(dataset, queryTranscript, str(queryYear), reference)


"""


_, dataset, reference = \
   hansardHandler.budgetToBow(1999, 2017, None, partyFunction, True, True, False, bowDirectory)
KlHansardIterative(dataset, reference)
