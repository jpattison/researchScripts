import re
import xml.etree.ElementTree as ET
from unidecode import unidecode
from cucco import Cucco
from string import digits
import nltk
# two following are to return the entire text as single string
nltkWords = set(nltk.corpus.words.words())
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
    
stop_words = set(stopwords.words('english'))
from nltk.stem.porter import *
def readOldText(root):
    # for prev_2011 returns a lower case version of the html contents.
    # all non-digit / non-letter characters are removed
    # appears to return it as a list

    output = ""
    for para in root.iter('para'):
        ascii_text = remove_non_ascii(para.text)
        ascii_text = returnSentences(ascii_text)
        if ascii_text:
            output += " " + ascii_text

    return [output]

def readNewText(root):
    # for post 2011 returns lowercase version of html contents.
    # all non-digit / non-letter characters are removed
    # appears to return it as a list

    output = ""
    for para in root.iter('talk.text'):     
        text = getDebateText('', para)

        ascii_text = remove_non_ascii(text)
        ascii_text = returnSentences(ascii_text)
        
        if ascii_text:
            output += " " + ascii_text
    return [output]




def getDebateText(current, element):
    # used for reading new hansard format
    # sort of loops through and merges the sub elements into one
    if element.text is not None:
        current = current + element.text
    for child in element:
        current = getDebateText(current, child)
    return current


# read transcript and break by paragraphs

def readOldPara(root):
    output = []
    for para in root.iter('para'):
        ascii_text = remove_non_ascii(para.text)
        if ascii_text:
            output.append(ascii_text)

    return output

def readNewPara(root):
    output = []

    for para in root.iter('talk.text'):     
        text = getDebateText('', para)
        text = re.sub('[\s]+',' ',text)

        ascii_text = remove_non_ascii(text)
        
        if ascii_text:
            output.append(ascii_text)

    return output


def remove_non_ascii(text):
    #print(text)

    if text:
        return unidecode(text)
    return None
    #return unidecode(unicode(text, encoding = "utf-8"))


def returnOnlyText(text):
    # returns only letters and digits in lowercase format. 
    # all other characters removed
    output = ""
    if not text:
        return output
    for i in text:
        if i.isalpha():
            output+=i.lower()
        else:
            output += " "
    return output

def returnNormalised(text):
    # uses cucco to perform normalisation. All stop words are removed it deals with morphologies
    # also remove wall digits
    cucco = Cucco()
    textNormalised = cucco.normalize(text)
    #digitsRemoved = textNormalised.translate(None, digits)
    digitsRemoved = re.sub(r'\d+', '', textNormalised)
    normalised = " ".join(w for w in nltk.wordpunct_tokenize(digitsRemoved) \
         if w.lower() in nltkWords)
    return normalised


def returnSentences(text):
    # appears to be nearly identicle to return only text except for a silly attempt of removing additoinal spacing
    # returns only letters and digits in lowercase format. 
    # all other characters removed
    output = ""
    if not text:
        return output
    for i in text:
        if i.isalpha():
            output+=i.lower()
        elif i==" " or i.isdigit():
            output += i
        else:
            output += ". "
    output = re.sub('(\s\.){2,}',' ',output)
    output = re.sub('(\s){2,}',' ', output)
    return output

def keepCommonText(text):
    # remove all words that start with capital letter (except start sentence) or have punctuations
    # return in list of lists, each list is a sentence
    if not text:
        return []

    #print(text)
    output = []

    global stop_words

    text = remove_non_ascii(text)
    for sentence in nltk.tokenize.sent_tokenize(text):
        first = True
        minPut =[]
        #print sentence
        for word in sentence.split(" "):
            word = word.strip(".,?-\"'")
            if len(word)== 0 or not ((first or word.islower())) or not word.isalpha() or word.lower() in stop_words:
                # word has capital letter and not first in sentence or contain non-letter characters or is a stop word
                # then skip
                first = False
                continue
            first = False
            if len(word) == 1:
                # so we can assume it has multiple characters
                minPut.append(word.lower())
                continue
            if not word[1:].islower():
                # really on if its start of sentence and a letter outside first is upper case
                continue
            minPut.append(word.lower())
        output.append(minPut)
    return output




def updatedReadOldText(root):
    # a differnet version of text normalisation
    # approach is remove non capital words (except start of sentence)
    # and words with hyphens or other characters in it
    # not doing porter stemming yet

    sentences = [] # list of lists. Each list is a sentence
    for para in root.iter('para'):
            normalised = keepCommonText(para.text)
            if normalised:
                sentences.extend(normalised)

    return sentences


def updatedReadNewText(root):
    # same as updatedReadOldText

    sentences = []


    sentences = [] # list of lists. Each list is a sentence
    for para in root.iter('talk.text'):
            text = getDebateText('', para)
            normalised = keepCommonText(text)
            if normalised:
                sentences.extend(normalised)
    return sentences

def stemParagraph(para):
    stemmer = PorterStemmer()
    output = []
    for sentence in para:
        stemmedSentence = []
        for word in sentence:
            stemmedSentence.append(stemmer.stem(word))
        output.append(stemmedSentence)

    

    return output    
