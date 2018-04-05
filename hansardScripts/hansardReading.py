import re
import xml.etree.ElementTree as ET
from unidecode import unidecode


# two following are to return the entire text as single string
def readOldText(root):
    output = ""
    for para in root.iter('para'):
        ascii_text = remove_non_ascii(para.text)
        if ascii_text:
            output += " " + ascii_text

    return [output]

def readNewText(root):
    output = ""
    for para in root.iter('talk.text'):     
        text = getDebateText('', para)
        text = re.sub('[\s]+',' ',text)

        ascii_text = remove_non_ascii(text)
        
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

    for i in text:
        if i.isalpha():
            output+=i
        else:
            output += " "
    return output