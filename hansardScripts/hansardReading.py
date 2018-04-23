import re
import xml.etree.ElementTree as ET
from unidecode import unidecode
from cucco import Cucco
from string import digits
import nltk
# two following are to return the entire text as single string
nltkWords = set(nltk.corpus.words.words())


def readOldText(root):
    output = ""
    for para in root.iter('para'):
        ascii_text = remove_non_ascii(para.text)
        ascii_text = returnSentences(ascii_text)
        if ascii_text:
            output += " " + ascii_text

    return [output]

def readNewText(root):
    output = ""
    for para in root.iter('talk.text'):     
        text = getDebateText('', para)
        #text = re.sub('[\s]+',' ',text)

        ascii_text = remove_non_ascii(text)
        ascii_text = returnSentences(ascii_text)
        
        if ascii_text:
            output += " " + ascii_text
    return [output]




def getDebateText(current, element):
    # used for reading new hansard format
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
    cucco = Cucco()
    textNormalised = cucco.normalize(text)
    #digitsRemoved = textNormalised.translate(None, digits)
    digitsRemoved = re.sub(r'\d+', '', textNormalised)
    normalised = " ".join(w for w in nltk.wordpunct_tokenize(digitsRemoved) \
         if w.lower() in nltkWords)
    return normalised


def returnSentences(text):
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

