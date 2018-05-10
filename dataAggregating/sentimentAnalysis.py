import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
nltk.download('vader_lexicon')
import json


def sentStats(sentences, buffer):
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
        else:
            print "error"
            print ss
            print sentence
            print ""
    return output, investigate

file = open("/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/sentences/2015-03-02.json")
sentences = json.loads(file.readline())

output, investigate = sentStats(sentences, 0.5)
print output
print investigate["positive"]
print "\n\n"
print investigate["negative"]