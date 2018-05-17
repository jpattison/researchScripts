import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
nltk.download('vader_lexicon')
import json
import hansardHandler
import graphs
sentenceLocation = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/sentences/"

def sentStats(sentences):
    # for each sentence calculate the sentiment
    # return number of positive, negative and neutral
    # as well as total
    sid = SentimentIntensityAnalyzer()
    output = {}

    investigate = {"positive" : [], "negative" : []}

    output["totPos"] = 0.0
    output["totNeg"] = 0.0
    output["totNeu"] = 0.0

    output["numPos"] = 0
    output["numNeg"] = 0
    output["numNeu"] = 0

    for sentence in sentences:
        ss = sid.polarity_scores(sentence)
        pos = ss['pos']
        neg = ss['neg']
        neu = ss['neu']
        output["totPos"] += pos
        output["totNeg"] += neg
        output["totNeu"] += neu

        #print sentence
        #print ss

        if pos > neg and pos > neu:
            output["numPos"] += 1
            investigate["positive"].append(sentence)
        elif neg > neu and neg > pos:
            investigate["negative"].append(sentence)
            output["numNeg"] += 1
        elif neu > neg and neu > pos:
            output["numNeu"] += 1
        # else:
        #     print "error"
        #     print ss
        #     print sentence
        #     print ""
    return output, investigate

def compareSentiments(initYear, finalYear, source = sentenceLocation):


    years = [year for year in range(initYear, finalYear+1)]

    # getBudgets(years, source, budgetSession = False, budgetEstimates = False, skipFirstDay = False)
    files = hansardHandler.getBudgets(years, source, False, True, False)

    counts = {}
    counter = 0
    print years
    print files
    for clump in files:
        year = years[counter]
        print year
        counts[year] = {}
        counts[year]["totPos"] = 0
        counts[year]["totNeg"] = 0
        counts[year]["total"] = 0
        for filename in clump:
            file = open(source+filename)
            sentences = json.loads(file.readline())
            counts[year]["total"]+=len(sentences)
            tCounts, tInvestigate = sentStats(sentences)

            counts[year]["totPos"] += tCounts["totPos"]
            counts[year]["totNeg"] += tCounts["totNeg"]
        counter += 1
    
    output = []
    keys = []
    for year in years:
        keys.append(["percPos", "percNeg"])
        temp = []
        temp.append(counts[year]["totPos"]*1.0/counts[year]["total"])
        temp.append(counts[year]["totNeg"]*1.0/counts[year]["total"])
        output.append(temp)

    return output, years, keys

#budgetWeek2012To2017
#budgetEstimates2012To2017
#budgetSentiment
results, years, keys= compareSentiments(2012, 2017)
print results
print years
print keys
graphs.setSubplots(keys, years, "Sentiment Hansard", results )