import cosineComparison
from datetime import datetime

bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised/"
# referenceFile = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised/2014-05-13.json"
referenceFile = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised/2015-05-12.json"



scores = cosineComparison.calculateSingleReference(bowDirectory, referenceFile, 100)

#print scores

# dicForm = cosineComparison.cosineToDicForm(scores)

# cosineComparison.graphByMonthYearGraph(dicForm, "frequency count", "accumulative scores" )

r1 = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised/2014-05-13.json"
r2 = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised/2014-05-14.json"
r3 = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised/2014-05-15.json"

references = [r1, r2, r3]

dicScore = cosineComparison.scoreMultipleReferenceDic(bowDirectory, references, 100)

sortedScore = cosineComparison.dicScoreToSortedList(dicScore)

# print sortedScore


count = 20
for score in scores:
    count -= 1
    # date = score[0]
    dateString = score[0]
    
    date = datetime.strptime(dateString, '%Y-%m-%d')
    print date.strftime("%d-%m-%Y")
    if count == 0:
        break