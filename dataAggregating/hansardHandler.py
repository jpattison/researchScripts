"""
Idea I want to pull out a specific set of hansard documents.

Output should generally be bag of words of corpus, query and a reference

"""

from datetime import timedelta, date, datetime

# bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised2/"
bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/byParty/bowNormalisedAndStemmed/"


import json

import os



politicalCalandar = {
    1999: { 
        "budget": [date(1999, 05, 11), date(1999, 05, 13)],
        "estimates" : [date(1999, 05, 31), date(1999, 06, 10)]       
    },  

    2000: { # not as sure for 2000
        "budget": [date(2000, 05, 9), date(2000, 05, 11)],
        "estimates" : [date(2000, 05, 29), date(2000, 06, 8)]       
    },

    2001: {
        "budget": [date(2001, 05, 22), date(2001, 05, 24)],
        "estimates" : [date(2001, 06, 4), date(2001, 06, 07)]       
    },


    2002: {
        "budget": [date(2002, 05, 14), date(2002, 05, 16)],
        "estimates" : [date(2002, 05, 27), date(2002, 06, 06)]       
    },
    
    2003: {
        "budget": [date(2003, 05, 13), date(2003, 05, 15)],
        "estimates" : [date(2003, 05, 26), date(2003, 06, 06)]       
    },

    2004: {
        "budget": [date(2004, 05, 11), date(2004, 05, 13)],
        "estimates" : [date(2004, 05, 24), date(2004, 06, 04)]        

    },

    2005: {
        "budget": [date(2005, 05, 10), date(2005, 05, 12)],
        "estimates" : [date(2005, 05, 23), date(2005, 06, 03)]
    },
    2006: {
        "budget": [date(2006, 05, 9), date(2006, 05, 11)],
        "estimates" : [date(2006, 05, 22), date(2006, 06, 01)]
    },
    2007: {
        "budget": [date(2007, 05, 8), date(2007, 05, 10)],
        "estimates" : [date(2007, 05, 21), date(2007, 05, 31)]
    },
    2008: {
        "budget": [date(2008, 05, 13), date(2008, 05, 15)],
        "estimates" : [date(2008, 05, 26), date(2008, 06, 05)]
    },    
    2009: {
        "budget": [date(2009, 05, 12), date(2009, 05, 14)],
        "estimates" : [date(2009, 05, 25), date(2009, 06, 04)]
    },
    2010: {
        "budget": [date(2010, 05, 11), date(2010, 05, 13)],
        "estimates" : [date(2010, 05, 24), date(2010, 06, 03)]
    },
    2011: {
        "budget": [date(2011, 05, 10), date(2011, 05, 12)],
        "estimates" : [date(2011, 05, 23), date(2011, 06, 02)]
    },
    2012: {
        "budget": [date(2012, 05, 8), date(2012, 05, 10)],
        "estimates" : [date(2012, 05, 21), date(2012, 05, 31)]
    },
    2013: {
        "budget": [date(2013, 05, 14), date(2013, 05, 16)],
        "estimates" : [date(2013, 05, 27), date(2013, 06, 06)]
    },    
    2014: {
        "budget": [date(2014, 05, 13), date(2014, 05, 15)],
        "estimates" : [date(2014, 05, 26), date(2014, 06, 05)]
    },
    2015: {
        "budget": [date(2015, 05, 12), date(2015, 05, 14)],
        "estimates" : [date(2015, 05, 25), date(2015, 06, 04)]
    },

    2016: {
        "budget": [date(2016, 05, 03), date(2016, 05, 04)],
        "estimates" : [date(2016, 05, 05), date(2016, 05, 06)]
    },
    2017: {
        "budget": [date(2017, 05, 9), date(2017, 05, 11)],
        "estimates" : [date(2017, 05, 22), date(2017, 06, 01)]
    }               
}

# set of dates of elections and who won. Starting at 1996. Idea is find the one previous election to find out who is in governmetn
coalition = ["lp", "nats", "np", "nayswa", "npacting", "clp"]
labor = ["alp"]


electionCalander = [(date(1996, 03, 11), coalition), (date(2007, 12, 03), labor), (date(2013, 9, 18), coalition)]


def partyInCharge(fileDate):
    # return a list parties in charge given a date. Only works for dates post 1996
    global electionCalander
    parties = None
    for (electionDate, electionWinner) in electionCalander:
        if electionDate <= fileDate:
            parties = electionWinner
        else:
            break
    return parties

def partyInOpposition(fileDate):
    global labor
    global coalition

    govParty = partyInCharge(fileDate)
    parties = None

    if govParty == coalition:
        parties = labor
    elif govParty == labor:
        parties = coalition
    return parties    



# I suppose the basic would be convert an entire year into single bag of words and use that
#def getHansard(initialYear, finalYear, queryYear, source=bowDirectory)

def daterange(start_date, end_date ):
    for n in range(1 + int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def month_year_iter(start_month, start_year, end_month, end_year ):
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for ym in range( ym_start, ym_end ):
        y, m = divmod( ym, 12 )
        yield y, m+1


def inbetweenDates(filename, budgetSession = False, budgetEstimates = False, both=False) :
    # im using this for trec stuff
    # for a given file, does it fall in a budget period

    if type(filename)==str:
        fileDate = getFileDate(filename)

        
    elif type(filename) == date:
        fileDate = filename
    elif type(filename) == datetime:
        fileDate = filename.date()
    else:
        print "error"
        print filename
        print type(filename)
    year = fileDate.year
    if year in politicalCalandar:
        if budgetSession:
            (start, finish) = politicalCalandar[year]["budget"]
            if fileDate>=start and fileDate<= finish:
                return True
        if budgetEstimates:
            (start, finish) = politicalCalandar[year]["estimates"]
            if fileDate>=start and fileDate<= finish:
                return True   
        if both:
            # just return if its within
            (start, _) = politicalCalandar[year]["budget"]
            (_, finish) = politicalCalandar[year]["estimates"]
            if fileDate>=start and fileDate<= finish:
                return True               
    return False         

def withinDates(initialDate, finalDate, bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised2/"):
    # assume in date format
    output = []
    for single_date in daterange(initialDate, finalDate):
        filename = single_date.strftime("%Y-%m-%d") + ".json"
        filepath = bowDirectory+filename
        if os.path.isfile(filepath):
            output.append(filename)

    return output

def getBudgets(years, source, budgetSession = False, budgetEstimates = False, skipFirstDay = False):
    #skip first days infers skip budget day as budget is released at night
    #years is a list
    output = []
    for year in years:
        tempYear = []
        if budgetSession:
            dates = politicalCalandar[year]["budget"]
            if skipFirstDay:
                print dates
                dates[0] += timedelta(days=1)
            tempYear.extend(withinDates(dates[0], dates[1], source))
        if budgetEstimates:
            dates = politicalCalandar[year]["estimates"]
            tempYear.extend(withinDates(dates[0], dates[1], source))
        output.append(tempYear)
    return output



# only cares about the budgets
# return bag of words of the budgets
def budgetToBow(initialYear, finalYear, queryYear, partyFunction, budgetSession = False, budgetEstimates = False, skipFirstDay = False, source=bowDirectory):
    years = []
    for year in range(initialYear, finalYear +1):
        if year != queryYear:
            years.append(year)
    dataFiles = getBudgets(years, source, budgetSession, budgetEstimates, skipFirstDay)

    reference, dataset = arrayToBow(dataFiles, partyFunction, source)
    if queryYear :
        queryFiles = getBudgets([queryYear], source, budgetSession, budgetEstimates, skipFirstDay)

        _, queryTranscript = arrayToBow(queryFiles, partyFunction, source)
        queryTranscript = queryTranscript[0]
    else:
        queryTranscript = None
    

    return queryTranscript, dataset, reference 

"""
def monthToBow(initialYear, finalYear, source=bowDirectory):
    # want a bag of words representation of all years, split by months 
    reference = {}
    count = 0
    iterator = month_year_iter(1, initialYear, 1, finalYear+1)
    sYear, sMonthInt = iterator.next()
    startDate = date(sYear, sMonthInt, 1)

    fileList = []
    for year, monthInt in iterator:
        #monthYear = startDate.strftime("%B - %Y")
        
        nextDate = date(year, monthInt, 1)
        reference[count] = startDate
        fileList.append(withinDates(startDate, nextDate, source))
        startDate = nextDate
        count += 1

    _, bows = arrayToBow(fileList, source)
    return reference, bows
"""

def folderToBow(folder):
    reference = {} 
    i = 0
    documents = []
    for filename in os.listdir(folder):
        split = str(filename).split('.')
        extension = split[-1].lower()
        date = split[0]
        if extension != 'json':
            continue

        filePath = folder+'/'+filename
        inputFile = open(filePath)
        bow = json.loads(inputFile.readline())
        documents.append(bow)
        reference[i]=date
        i +=1
    return reference, documents
    vectorizer = DictVectorizer()
    matrix = vectorizer.fit_transform(documents)
    return reference, matrix, vectorizer

def arrayToBow(docArray, partyFunction, folder=None):
    # same as folderToBow but assumes a list of lists for documents
    # if multiple documents in same inner list then merge. But like by putting individual we can easily just use as a singular as well
    
    """
    Given a list of list of documents. I want to return a list of bag of words. We assume each list of list corresponds to a 
    set of documents in the same year. We want to merge those in the same year to a big bag of words.


    At the same time there's an associated partyFunction of the parties we want to grab the documents from

    """

    documents = []
    i = 0
    reference = {}
    for docSet in docArray:
        #print docSet
        doc = {}
        # print "newDoc size = {0}".format(len(doc))
        name = None
        for filename in docSet:
            
            if name == None:

                name = filename
                print name
                print len(docSet)

                # print name
                reference[i]=int(name[:4])
                i+=1
            if folder:
                tempFile = open(folder+filename)
            else:
                tempFile = open(filename)
            
            hansardByParty = json.loads(tempFile.readline())

            # sane amount
            #numberOfWordsInPartyBow(hansardByParty)
            

            parties = partyFunction(filename)

            bowPartiesMerged = retrieveBowFromParties(hansardByParty, parties)
            # now add the bow to the year combined
            addToDictionary(doc, bowPartiesMerged)
            

        documents.append(doc)
    return reference, documents

def numberOfWordsInPartyBow(partyBow):
    total = 0
    for party in partyBow:
        total += countWords(partyBow[party])
    print "{0} words detected total".format(total)

def countWords(bow):
    subTotal = 0
    for word in bow:
        subTotal += bow[word]
    return subTotal 

def fileToBow(fileLocation):
    file = open(fileLocation)
    bow = json.loads(file.readline())
    return bow


def retrieveBowFromParties(hansardByParty, interestedParties):
    output = {}

    for party in hansardByParty:
        if party.lower() in interestedParties:
            addToDictionary(output, hansardByParty[party])
    return output

def addToDictionary(addTo, addFrom):
    for word in addFrom:
        if not word in addTo:
            addTo[word] = 0
        addTo[word] += addFrom[word]


"""
bugs were due to these two things. Redoing above
def grabReleventBows(partyBow, parties, outputBow = {}):
    ### Given new format of split by party this may cause issues.
    #print partyBow.keys()
    for party in partyBow:
        if party.lower() in parties:
            mergeBow(outputBow, partyBow[party])
    return outputBow

def mergeBow(primary, toAdd):
    for key in toAdd:
        if not key in primary:
            primary[key] = 0
        primary[key] += toAdd[key]
"""

def getFileDate(filename):
    #given filename. Determine the date
    parts = filename.split('.')
    fileDate = datetime.strptime(parts[0],"%Y-%m-%d").date()
    return fileDate

def filenameToPartyInCharge(filename):
    fileDate = getFileDate(filename)
    return partyInCharge(fileDate)

def fileNameToOppsition(filename):
    fileDate = getFileDate(filename)
    return partyInOpposition(fileDate)

def returnSpecificParty(partyList):
    def ignoreInput(something):
        return partyList
    return ignoreInput

