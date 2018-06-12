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

customStopWords = ["honourable", "member", "government", "question", "answer"]
import wNormalisation
import re


from nltk.stem.porter import *
stemmer = PorterStemmer()


def convertToAscii(text):
    # converts to ascii
    if text:
        return unidecode(text)
    return None

# def normaliseWord(word):
#     # return only letters and lowercase
#     word = word.lower()
#     output = ""
#     for letter in word:
#         if letter.isalpha():
#             output+=letter

#     return output

def getStemmed(words):
    #given list of words. return the stemmed versions
    global stemmer
    output = []
    for word in words:
        output.append(stemmer.stem(word))
    return output

def removeStopWords(words):
    # assume input is simply a list of words. Want to keep normal words only
    # do i want to remove all capital words?
    global stop_words
    output = []
    
    for word in words:
        

        if len(word) <= 1 or word in stop_words:
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

def stripCapitalisedWords(words):
    # remove all words that start with upper case except first
    if len(words) <= 1:
        return words
    output = [words[0]]
    for word in words[1:]:
        if word[0].islower():
            output.append(word)
    return output

def lowerCaseList(inputList):
    output = []
    for word in inputList:
        output.append(word.lower())
    return output

def sentencesToNormalised(document, removeCapitals, stemWords): #, removeCapitals=False, stemWords = False):
    # assume string with character normalisation already done.
    # produces list of words broken by sentences
    # normalisation is remove of stopwords and words length 1 such as "s" or "a'"
    # optionally remove all capital words after first
    output = []
    sentences = sent_tokenize(document)

    for sentence in sentences:
        words = word_tokenize(sentence)
        if removeCapitals:
            words = stripCapitalisedWords(words)
        words = lowerCaseList(words)
        words = removeStopWords(words)
        
        if stemWords:
            words = getStemmed(words)

        output.append(words)
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


def normaliseText(document):
    # been given a list of strings. Want to perform some preformatting.
    # Normalisations:
    # 1) Remove all nonalpha characters apart from sentence structure ones
    # 2) convert to ascii
    # 3) Remove excessive spaces but that shouldn't matter
    output = []
    
    #print "\n\n yet another"
    #print document
    for subDocument in document:
        if not subDocument:
            # is a Nothing object
            continue

        #normalised = 
        normalised = normaliseString(subDocument)
        #normalised = re.sub('[\s]+',' ',normalised)
        output.append(normalised)
    return output

def normaliseString(inputString):
    # we're given a string that is likely a list of sentences. 
    # I want to remove all nonalpha numeric characters but keep the fullstops
    output = ""

    inputString = convertToAscii(inputString) # turn to ascii
    for sentence in sent_tokenize(inputString):
        for word in word_tokenize(sentence):
            #print word
            for character in word:
                if character.isalpha() or character in ".,!;":
                    output += character
                else:
                    output += " "
            output += " " # space bween words
        #output += ". " # fullstop between sentence
    
    output = re.sub('[\s]+',' ',output)
    return output


