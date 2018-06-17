import xml.etree.ElementTree as ET
import readNewHansard
import os
import json
import sys
sys.path.insert(0, '/Users/jeremypattison/LargeDocument/scripts/dataAggregating')
import hansardHandler
from unidecode import unidecode



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
        title = unidecode(title)
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

def traceBill(startYear, endYear, billTitles, removeCapitals, stemWords):
    """
    Given a year and a set of billTitles (in case of multiple names for same one)
    produce a dicitionary of all speeches 

    """

    # outputFileName = billTitles[0]
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    
    billTracker = {"speechesByDate":{}, "startYear":startYear, "firstDetected": None}

    for year in range(startYear, endYear+1):
        yearStr = str(year)
        input_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/{0}".format(yearStr)

        for filename in os.listdir(input_directory):
            split = str(filename).split('.')
            extension = split[-1].lower()
            if extension != 'xml':
                continue
            dateStr = split[0]
            dateDateFormat = hansardHandler.getFileDate(filename)


            fileLocation = input_directory+'/'+filename
            #print fileLocation
            speechesOnDate = billOnDateByMp(fileLocation, billTitles, removeCapitals, stemWords)
            if speechesOnDate:
                if not billTracker["firstDetected"] or billTracker["firstDetected"] > dateDateFormat:
                    billTracker["firstDetected"] = dateDateFormat
                billTracker["speechesByDate"][dateStr]= speechesOnDate
    
 

    return billTracker


def allBillsOnBudget(year):
    """
    returns all the bills that are mentioned during budget
    """

    titleBills = []
    input_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/{0}".format(year)
    for filename in os.listdir(input_directory):

            split = str(filename).split('.')
            extension = split[-1].lower()
            if extension != 'xml':
                continue
            date = split[0]
            fileLocation = input_directory+'/'+filename
            if not hansardHandler.inbetweenDates(filename, True, False, False):
                continue
            titleBills.extend(grabBillTitles(fileLocation))
    print "{0} bills detected".format(len(titleBills))
    return titleBills




def grabBillTitles(inputFile):

    """ 
    Return all bills mentioned in a day of parliament

    """
    
    tree = ET.parse(inputFile)
    root = tree.getroot()
    bills = root.findall(".//debateinfo[title='BILLS']/../subdebate.1")
    
    titles = []
    
    for subdebate in bills:

        

        #print subdebate
        title = subdebate.find('subdebateinfo/title').text
        #print title.lower()
        titles.append(unidecode(title).lower())
    return titles



def speechForBudgetMeasure(year, removeCapitals, stemWords, skipFirstDay):
    """
    1) For the specific year grabs all bills mentioned through that budget
    2) Goes through the year and groups the speeches with the bills and date
    3) If the bill is first mentioned during the budet time then we save it
    4) Saves to output

    To do a seperate one:
    3) Scans through the data now and any bill that has mention of on first day of budget or before is removed
        we remove first day of budget as bills aren't introduced until second day
    4) Also doesn't attach the speech for any during the budget week / budget estimate. Cause don't want to to mix them up

    """

    global outputDirectory

    bills = allBillsOnBudget(year)
    #print bills

    allBills = {}

    cutOffDate = hansardHandler.politicalCalandar[year]["budget"][0] # the first day of budget
    print cutOffDate

    for bill in bills:
        # if len(bill) > 200:
        #     print "\nskipped {0}\n".format(bill)
        #     continue

        print "\n\ndoing {0}".format(bill)
        associatedSpeech = traceBill(year, year, [bill], removeCapitals, stemWords)
        firstDetected = associatedSpeech["firstDetected"]
        # print "first date is {0} ".format(firstDetected)
        # print "cutoff date is {0}".format(cutOffDate)
        # print firstDetected<= cutOffDate
        print firstDetected
        if not firstDetected:
            print "can't find a speech"
            continue
        elif skipFirstDay and firstDetected<= cutOffDate:
            print "skipping as mentioned before budget"
            continue
        elif not skipFirstDay and firstDetected < cutOffDate:
            print "skipping as mentioned before budget"
            continue
        print "Success \n\n\n"
        associatedSpeech["firstDetected"] = firstDetected.strftime("%Y-%m-%d")
        allBills[bill] = associatedSpeech
        #print associatedSpeech

    outputFileDirectory = outputDirectory+str(year)+".json"
    outputFile = open(outputFileDirectory, 'w')
    json.dump(allBills, outputFile)   


#billTitles = ["australian national preventive health agency (abolition) bill 2014"]
#billTitles = ["private health insurance amendment bill (no. 1) 2014"]
#billTitles = ["Export Inspection (Service Charge) Amendment Bill 2014".lower()]

#speeches = billOnDateByMp(input_file, billTitles)

"""
billTracker = traceBill(2014,2014, billTitles, "pass", True, True)
print billTracker.keys()
print "found for these dates"

print billTracker["speechesByDate"].keys()
for debateDate in billTracker["speechesByDate"]:
    print debateDate
"""

"""
allBill = allBillsOnBudget(2014)


for bill in allBill:
    if bill == "australian national preventive health agency (abolition) bill 2014":
        print bill
        print "\n"
"""

for i in range(2012,2016):
    speechForBudgetMeasure(i, True, True, False)


# print traceBill(2014, 2014, ["australian national preventive health agency (abolition) bill 2014"], True, True)


"""
specificDay = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/2014/2014-05-15.xml"

customBills = grabBillTitles(specificDay)

for customBill in customBills:
    print customBill

"""