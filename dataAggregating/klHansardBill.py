"""
I've been given a bill and a year. I want to find the KL between the parties in budget weeks and bill

"""

import json
import hansardHandler
import cosineComparison


hansardSource = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/byParty/bowNormalisedAndStemmed/"

billSource = "/Users/jeremypattison/LargeDocument/ResearchProjectData/hansardBills/"

coalition = ["lp", "nats", "np", "nayswa", "npacting", "clp"]
labor = ["alp"]




def retrieveBillBow(billFile, parties):
    inputFile = open(billFile)
    billTracker = json.loads(inputFile.readline())
    print billTracker.keys()
    partyBow = {}
    startYear =  billTracker["startYear"]
    speechByDate = billTracker["speechesByDate"]
    for debateDate in speechByDate:
        print debateDate
        hansardHandler.grabReleventBows(speechByDate[debateDate], parties, partyBow)
    return partyBow, startYear


def investigateBill(billSource, billTitle):
    print billTitle
    billFile = billSource + billTitle + ".json"

    interestedParty = coalition
    partyFunction = hansardHandler.returnSpecificParty(interestedParty)
    partyBillBow, startYear = retrieveBillBow(billFile, interestedParty)

    # note we choose startYear, startYear as only interested in that year
    _, hansardBows, hansardReference  = hansardHandler.budgetToBow(startYear, startYear, None, partyFunction, True, True, False, hansardSource)

    assert len(hansardBows) == 1
    hansardBow = hansardBows[0]

    print cosineComparison.KLbow(hansardBow, partyBillBow)

#billTitle = "australian national preventive health agency (abolition) bill 2014"
billTitle = "private health insurance amendment bill (no. 1) 2014"
investigateBill(billSource, billTitle)