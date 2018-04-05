"""
Specify a set of hansard documents and convert into a text document
"""

import hansardReading
import xml.etree.ElementTree as ET
import re

def singleDocumentToText(fileLocation, isNew):
    input_file = open(fileLocation)
    tree = ET.parse(input_file)
    if isNew:
        textArray = hansardReading.readNewText(tree.getroot())
    else:
        textArray = hansardReading.readOldText(tree.getroot())
    text = ""
    for element in textArray:
        text += element
    text = re.sub('[\s\n\r]+',' ',text)


    return text


condensed = singleDocumentToText("/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/2014/2014-05-14.xml", True)

outputFile = open("/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/textSnippits/2014-05-14.txt", 'w')

outputFile.write(condensed)