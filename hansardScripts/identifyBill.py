import xml.etree.ElementTree as ET
import readNewHansard
import os
import json
import sys
sys.path.insert(0, '/Users/jeremypattison/LargeDocument/scripts/dataAggregating')
import hansardHandler



"""
Idea is we want to have bill, maybe as a list. Each time is a time that the bill was debated on. Idea 
is to be able to compare the final debate to the first one. Keep track of all mps and their parties and their dates.

Our structure is a dictionary:
Keys:
    BillName
    Outcome
    Date
        (MP name, nameId, MP party) : Speech

Plan is to iterate between two dates we already know. Grab the debate and then save in a file

How did government frame it, how did opposition frame it.

Difference in entropy of government speeches, opposition speeches. Topic modelling?

Language model being budgetweek, how much did they diverge?
"""


# input_file = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/2012/2012-06-19.xml"
# input_file = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/2014/2014-06-03.xml"

outputDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/hansardBills/"


def billOnDateByMp(inputFile, billTitles, removeCapitals, stemWords):

    """ for a specific hansard date group all the speeches by mps on the bill into one
    This produces the "speeches" part of structure

    """
    
    tree = ET.parse(inputFile)
    root = tree.getroot()
    bills = root.findall(".//debateinfo[title='BILLS']/../subdebate.1")
    
    groupedSpeeches = {}
    
    for subdebate in bills:

        

        #print subdebate
        title = subdebate.find('subdebateinfo/title').text
        #print title.lower()
        if not title.lower() in billTitles:
            continue

        speeches = subdebate.findall('.//speech')
        for speech in speeches:
            associatedText = readNewHansard.readTalk(speech)
            if associatedText:
                readNewHansard.attatchSpeechToMp(groupedSpeeches, associatedText)



        #billSpeeches.append(debateSpeech)

    # now put it into format we want.
    byParty = readNewHansard.groupByParty(groupedSpeeches)
    bowParty = readNewHansard.bowByParty(byParty, removeCapitals, stemWords)
    return bowParty

def traceBill(startYear, endYear, billTitles, outcome, removeCapitals, stemWords, budgetMode =False):
    # if budgetMode we disgard all bills that appear before the budget add to corpus for ones that fall in it.
    global outputDirectory
    outputFileName = billTitles[0]
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    
    billTracker = {"billName":outputFileName, "outcome":outcome, "speechesByDate":{}, "startYear":startYear}

    for year in range(startYear, endYear+1):
        yearStr = str(year)
        input_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/{0}".format(yearStr)

        for filename in os.listdir(input_directory):
            split = str(filename).split('.')
            extension = split[-1].lower()
            if extension != 'xml':
                continue
            date = split[0]
            fileLocation = input_directory+'/'+filename
            print fileLocation
            speechesOnDate = billOnDateByMp(fileLocation, billTitles, removeCapitals, stemWords)
            if speechesOnDate:
                print "got something"
                billTracker["speechesByDate"][date]= speechesOnDate
    
    outputFileDirectory = outputDirectory+outputFileName+".json"
    outputFile = open(outputFileDirectory, 'w')
    json.dump(billTracker, outputFile)    

    return billTracker


def allBillsOnBudget(year):
    billsTitles = []
    input_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/{0}".format(year)
    for filename in os.listdir(input_directory):

            split = str(filename).split('.')
            extension = split[-1].lower()
            if extension != 'xml':
                continue
            date = split[0]
            fileLocation = input_directory+'/'+filename
            if not hansardHandler.inbetweenDates(filename, False, True, False):
                continue
            billsTitles.extend(grabBillTitles(fileLocation))
    print "{0} bills detected".format(len(billsTitles))
    for bill in billsTitles:
        print bill
        print ""




def grabBillTitles(inputFile):

    """ for a specific hansard date group all the speeches by mps on the bill into one
    This produces the "speeches" part of structure

    """
    
    tree = ET.parse(inputFile)
    root = tree.getroot()
    bills = root.findall(".//debateinfo[title='BILLS']/../subdebate.1")
    
    titles = []
    
    for subdebate in bills:

        

        #print subdebate
        title = subdebate.find('subdebateinfo/title').text
        #print title.lower()
        titles.append(title.lower())
    return titles

#billTitles = ["australian national preventive health agency (abolition) bill 2014"]
#billTitles = ["private health insurance amendment bill (no. 1) 2014"]
billTitles = ["Export Inspection (Service Charge) Amendment Bill 2014".lower()]

#speeches = billOnDateByMp(input_file, billTitles)


billTracker = traceBill(2014,2014, billTitles, "pass", True, True)
print billTracker.keys()
print "found for these dates"

print billTracker["speechesByDate"].keys()
for debateDate in billTracker["speechesByDate"]:
    print debateDate



#allBillsOnBudget(2014)
