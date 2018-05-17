### Very quick proof of concept of printing out the frequency of the word austerity from 2000


import sys

sys.path.insert(0, '/Users/jeremypattison/LargeDocument/scripts/dataAggregating')
import hansardHandler
import graphs
bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised2/"

# queryTranscript, dataset, reference = \
#    hansardHandler.budgetToBow(2005, 2017, None, False, True)

# #print queryTranscript

# print len(dataset)
# print reference

# for i in range(len(dataset)):
#     #print i
#     print reference[i]
#     if "austerity" in dataset[i]:
#         print dataset[i]["austerity"]
#     else:
#         print 0



reference, dataset = hansardHandler.monthToBow(2000, 2017, bowDirectory)

output = []
xticks = []
for i in range(len(dataset)):
    #print i
    xticks.append(reference[i])
    if "austerity" in dataset[i]:
        output.append(dataset[i]["austerity"])
    else:
        output.append(0)

print output
print xticks

graphs.lineOverTime(xticks, "frequency", "austerity over time", output)