"""
Idea I want to pull out a specific set of hansard documents.

Output should generally be bag of words of corpus, query and a reference

"""

from datetime import timedelta, date, datetime

bowDirectory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalised2/"


import json

import os



politicalCalandar = {
    
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
        parts = filename.split('.')
        fileDate = datetime.strptime(parts[0],"%Y-%m-%d").date() 
        
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
                dates[0] += datetime.timedelta(days=1)
            tempYear.extend(withinDates(dates[0], dates[1], source))
        if budgetEstimates:
            dates = politicalCalandar[year]["estimates"]
            tempYear.extend(withinDates(dates[0], dates[1], source))
        output.append(tempYear)
    return output



# only cares about the budgets
# return bag of words of the budgets
def budgetToBow(initialYear, finalYear, queryYear, budgetSession = False, budgetEstimates = False, skipFirstDay = False, source=bowDirectory):
    years = []
    for year in range(initialYear, finalYear +1):
        if year != queryYear:
            years.append(year)
    dataFiles = getBudgets(years, source, budgetSession, budgetEstimates, skipFirstDay)

    reference, dataset = arrayToBow(dataFiles, source)
    if queryYear :
        queryFiles = getBudgets([queryYear], source, budgetSession, budgetEstimates, skipFirstDay)

        _, queryTranscript = arrayToBow(queryFiles, source)
        queryTranscript = queryTranscript[0]
    else:
        queryTranscript = None
    

    return queryTranscript, dataset, reference 


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

def arrayToBow(docArray, folder=None):
    # same as folderToBow but assumes a list of lists for documents
    # if multiple documents in same inner list then merge. But like by putting individual we can easily just use as a singular as well
    documents = []
    i = 0
    reference = {}
    for docSet in docArray:
        doc = {}
        name = None
        for filename in docSet:
            if name == None:
                name = filename
                reference[i]=int(name[:4])
                i+=1
            if folder:
                tempFile = open(folder+filename)
            else:
                tempFile = open(filename)
            
            bow = json.loads(tempFile.readline())

            for key in bow:
                if key in doc:
                    doc[key] += bow[key]
                else:
                    doc[key] = bow[key]
        documents.append(doc)
    return reference, documents

def fileToBow(fileLocation):
    file = open(fileLocation)
    bow = json.loads(file.readline())
    return bow


 
