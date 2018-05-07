import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
nltk.download('vader_lexicon')
import json

"""
sentences = ["VADER is smart, handsome, and funny.", # positive sentence example
"VADER is smart, handsome, and funny!", # punctuation emphasis handled correctly (sentiment intensity adjusted)
"VADER is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
"VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
"VADER is VERY SMART, handsome, and FUNNY!!!",# combination of signals - VADER appropriately adjusts intensity
"VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!!",# booster words & punctuation make this close to ceiling for score
"The book was good.",         # positive sentence
"The book was kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
"The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
"A really bad, horrible book.",       # negative sentence with booster words
"At least it isn't a horrible book.", # negated negative sentence with contraction
":) and :D",     # emoticons handled
"",              # an empty string is correctly handled
"Today sux",     #  negative slang handled
"Today sux!",    #  negative slang with punctuation emphasis handled
"Today SUX!",    #  negative slang with capitalization emphasis
"Today kinda sux! But I'll get by, lol" # mixed sentiment example with slang and constrastive conjunction "but"
]


tricky_sentences = [
"Most automated sentiment analysis tools are shit.",
"VADER sentiment analysis is the shit.",
"Sentiment analysis has never been good.",
"Sentiment analysis with VADER has never been this good.",
"Warren Beatty has never been so entertaining.",
"I won't say that the movie is astounding and I wouldn't claim that \
the movie is too banal either.",
"I like to hate Michael Bay films, but I couldn't fault this one",
"It's one thing to watch an Uwe Boll film, but another thing entirely \
to pay for it",
"The movie was too good",
"This movie was actually neither that funny, nor super witty.",
"This movie doesn't care about cleverness, wit or any other kind of \
intelligent humor.",
"Those who find ugly meanings in beautiful things are corrupt without \
being charming.",
"There are slow and repetitive parts, BUT it has just enough spice to \
keep it interesting.",
"The script is not fantastic, but the acting is decent and the cinematography \
is EXCELLENT!",
"Roger Dodger is one of the most compelling variations on this theme.",
"Roger Dodger is one of the least compelling variations on this theme.",
"Roger Dodger is at least compelling as a variation on the theme.",
"they fall in love with the product",
"but then it breaks",
"usually around the time the 90 day warranty expires",
"the twin towers collapsed today",
"However, Mr. Carter solemnly argues, his client carried out the kidnapping \
under orders and in the ''least offensive way possible.''"]


paragraph = "It was one of the worst movies I've seen, despite good reviews. \
Unbelievably bad acting!! Poor direction. VERY poor production. \
The movie was bad. Very bad movie. VERY bad movie. VERY BAD movie. VERY BAD movie!"

lines_list = tokenize.sent_tokenize(paragraph)
sentences.extend(lines_list)
sentences.extend(tricky_sentences)
"""
sid = SentimentIntensityAnalyzer()

# for sentence in sentences:
#     print(sentence)
#     ss = sid.polarity_scores(sentence)
#     print ss
#     for k in sorted(ss):
#         print('{0}: {1}, '.format(k, ss[k]))
#     print()



def sentStats(sentences, buffer):
    # for each sentence calculate the sentiment
    # return number of positive, negative and neutral
    # as well as total
    sid = SentimentIntensityAnalyzer()
    output = {}
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

        print sentence
        print ss

        if pos > neg and pos > neu:
            output["numPos"] += 1
        elif neg > neu and neg > pos:
            output["numNeg"] += 1
        elif neu > neg and neu > pos:
            output["numNeu"] += 1
        else:
            print "error"
            print ss
    return output


file = open("/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/sentences/2015-03-02.json")
sentences = json.loads(file.readline())

output = sentStats(sentences, 0.5)

print output