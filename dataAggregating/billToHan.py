import json
import hansardBudgetAnalysis
import hansardHandler
from datetime import timedelta, date, datetime
bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/byParty/bowNormalisedAndStemmed/"


year = 2012

yearAsDate = date(year,1,1)

billFileLocation = "/Users/jeremypattison/LargeDocument/ResearchProjectData/hansardBills/2014.json"

billFile = json.loads(open(billFileLocation).readline())



partyFunction = hansardHandler.filenameToPartyInCharge


_, dataset, reference = \
   hansardHandler.budgetToBow(2005, 2017, None, partyFunction, True, True, False, bowDirectory)

print "cats"

partiesInCharge = hansardHandler.partyInCharge(yearAsDate)


bow = {}

for billTitle in billFile.keys():
    print billTitle
    bill = billFile[billTitle]
    

    speeches = bill["speechesByDate"]
    for speechDate in speeches.keys():
        print speechDate
        speech = speeches[speechDate]
        parties = speech.keys()
        for party in parties:
            print party
            if party.lower() in partiesInCharge:
                hansardHandler.addToDictionary(bow, speech[party])
    break

smoothing = True

hansardBudgetAnalysis.KLBackwardsGraph(dataset, bow, "cat", reference, smoothing)

