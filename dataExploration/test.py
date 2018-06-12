

import sys

sys.path.insert(0, '/Users/jeremypattison/LargeDocument/scripts/dataAggregating')

import hansardHandler

bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/byParty/bowNormalisedAndStemmed/"


partyFunction = hansardHandler.filenameToPartyInCharge


_, dataset, reference = \
   hansardHandler.budgetToBow(2015, 2017, None, partyFunction, True, True, False, bowDirectory)


print len(dataset)
print reference

for i in range(len(dataset)):
    data = dataset[i]
    total = 0
    print reference[i]

    print "words types = {0}".format(len(data))
    for word in data:
        total += data[word]
    print "word totals = {0}".format(total)