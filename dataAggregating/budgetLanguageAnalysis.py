import json
import cosineComparison
import graphs
bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised/"


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

budgets = [budget2005, budget2006, budget2007, budget2008, budget2009, budget2010, budget2011, budget2012, budget2013, \
  budget2014, budget2015, budget2016, budget2017]

referenceBudget = budget2008

budgets.remove(referenceBudget)
# note should i be oing TFIDF stuff or keep it pure?


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

# budgetList = [(budget2005, "budget2005"), (budget2006, "budget2006 Howard Last"), 
# (budget2007, "budget2007 Rudd First"), (budget2008, "budget2008"), (budget2011, "budget2011 Gillard first"), (budget2013, "budget2013 gillard last"),
# (budget2014, "budget2014"), (budget2017, "budget2017")]

# for budgetPair in budgetList:
#     budgets = [budget2005, budget2006, budget2007, budget2008, budget2009, budget2010, budget2011, budget2012, budget2013, \
#   budget2014, budget2015, budget2016, budget2017]    

#     referenceBudget = budgetPair[0]
#     budgets.remove(referenceBudget)
#     reference, documents = cosineComparison.arrayToBow(budgets, bowDirectory)

#     _, queryBow = cosineComparison.arrayToBow([referenceBudget], bowDirectory)

#     #matrix, query = cosineComparison.calculateComparison(documents, queryBow, k)
#     matrix, query = cosineComparison.matrixQueryNoTransformation(documents, queryBow[0])


#     #scores = cosineComparison.scoreDocuments(query, matrix, reference) # cosine
#     scores = cosineComparison.inverseKLdivergence(query, matrix, reference) #jointEntropy

#     xAxis = [pair[0][0:4] for pair in scores]
#     values = [pair[1] for pair in scores]
#     print scores
#     name = budgetPair[1]

#     graphs.makeGraph(xAxis, "scores", "budget log for {0}".format(name), values, name)


_, pBow = cosineComparison.arrayToBow([budget2014], bowDirectory)
_, qBow = cosineComparison.arrayToBow([budget2013], bowDirectory)

pBow, qBow = pBow[0], qBow[0]

klWords, missing = cosineComparison.KLdivergenceWords(pBow, qBow)

klWords = klWords.items()

klWords.sort(key=lambda x: x[1])

# print klWords[0:100]
# print("\n")
for wordPair in klWords[-100:]:
    word = wordPair[0]
    print("Word: {0} 2014: {1} 2013: {2}".format(word, pBow[word], qBow[word]))

# print "now lowest \n \n"
# for wordPair in klWords[0:100]:
#     word = wordPair[0]
#     print("Word: {0} P: {1} Q: {2}".format(word, pBow[word], qBow[word]))



# missing = missing.items()
# missing.sort(key=lambda x: x[1], reverse=True)
# print("\n\n")
# print missing[0:100]