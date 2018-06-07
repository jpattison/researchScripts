"""
We're fed a large amount of text. This deals with representation

It does not deal with hansard at all but can be fed hansard data


ToDo:

1 Remove all words starting capitals?
2 removing non alpha numeric codes needs to be done PRIOR to tokenisation so we can replace with spaces
3 lematise or remove wrods not in common dic?

"""
from unidecode import unidecode
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

import nltk
nltkWords = set(nltk.corpus.words.words())
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))


def convertToAscii(text):
    # converts to ascii
    if text:
        return unidecode(text)
    return None

def normaliseWord(word):
    # return only letters and lowercase
    word = word.lower()
    output = ""
    for letter in word:
        if letter.isalpha():
            output+=letter

    return output


def keepCommonWords(words):
    # assume input is simply a list of words. Want to keep normal words only
    # do i want to remove all capital words?

    output = []
    
    for word in words:
        word = normaliseWord(word)

        if word in stop_words:
            continue
        # if not word in nltkWords:
        #     print "removed " + word
        #     continue
        output.append(word)
    return output


def listToBOW(listOfWords, outDic):
    for word in listOfWords:
        if len(word)<1:
            continue
        if not word in outDic:
            outDic[word] = 0
        outDic[word] += 1
    return outDic




def sentencesToNormalised(string):
    # assume string, want output of words with normalisations
    output = []
    sentences = sent_tokenize(string)

    for sentence in sentences:
        words = word_tokenize(sentence)
        normalised = keepCommonWords(words)
        output.append(normalised)
    return output

def flattenList(lists):
    # want to return all values as single list
    output = []
    assert type(lists)==list

    for subList in lists:
        if type(subList)==list:
            output.extend(flattenList(subList))
        else:
            output.append(subList)
    return output



