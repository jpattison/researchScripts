"""
What Im trying to do here is see if we can group speeches by same people.

I'll focus on making it just for the new budget format (post april 2011)


TODO:

1) I don't think it is dealing with interjectinos
2) We found a large error with not getting opening part of a speech. I think its fixed but should investigate
3) I think we should be removing the non alpha characters here. Probably in normaliseText

"""
import xml.etree.ElementTree as ET
import wNormalisation
import re

def normaliseText(paragraph):
    # been given a list of strings. Want to perform some preformatting.
    # Ideally this is where i remove non-alphanumeric characters and replace with a space
    output = []
    
    #print "\n\n yet another"
    #print paragraph
    for sentence in paragraph:
        if not sentence:
            # is a Nothing object
            continue
        normalised = wNormalisation.convertToAscii(sentence)
        normalised = re.sub('[\s]+',' ',normalised)
        output.append(normalised)
    return output


def getTalkDetails(talkDic, talkStart):
    # Grab all attributes about the speaker
    # There's actually more generally in the poorly formatted below but this generally gets name/party
    talker = talkStart.find("./talker")
    for child in talker:
        talkDic[child.tag] = child.text


def fixXML(element):
    # I was having trouble with what I believe is incorrectly made xml This is a hacky way of removing a 
    # a bunch of tags that usually appear just before the first speech
    # these tags generally have some information about electorate and time

    # idea is we convert xml element back to string, string modification and hope we haven't broken xml
    ##print "\n\n yet another"
    #print element
    asText = ET.tostring(element)
    #print "before"
    #print asText
    asText = re.sub('\n\s*<a.*\n.*<span.*>\n.*</a>\s\(<span.+</span>\):', '', asText)
    #print "after"
    #print asText
    asElement = ET.fromstring(asText)
    return asElement


def getTalkText(talkDic, talkText):
    # we're trying to grab the speech associated with person.
    speech = []
    textElement = talkText.findall("./p/span")
    

    for texty in textElement:
        #print "prior"
        #print texty
        #print texty.text
        texty = fixXML(texty)
        #print "after"
        #print texty
        #print texty.text
        speech.append(texty.text)

    normalisedSpeech = normaliseText(speech)
    talkDic["speech"] = normalisedSpeech

def readTalk(talk):
    # associates the speaker with the text.

    talkDic = {}

    talkStart = talk.find("./talk.start")
    talkText = talk.find("./talk.text/body")

    if not talkText:
        # Generally interjections but from recollection more than that.
        # #print "skipped one. Investigate"
        return None

    getTalkDetails(talkDic, talkStart)
    getTalkText(talkDic, talkText)

    return talkDic

def attatchSpeechToMp(overallDic, individualSpeech):
    name = individualSpeech["name"]
    nameId = individualSpeech["name.id"]
    party = individualSpeech["party"]

    if not (name, nameId, party) in overallDic:
        overallDic[(name, nameId, party)] = []
    overallDic[(name, nameId, party)].append(individualSpeech["speech"])



def groupByMp(input_file):
    # Go through file and produce a mapping between all speeches to the MP.
    tree = ET.parse(input_file)
    root = tree.getroot()

    talks = root.findall(".//talk.start/..")

    overall = {}

    for talk in talks:

        speech = readTalk(talk)
        if speech:
            attatchSpeechToMp(overall, speech)

    return overall 

def groupByParty(byMpDic):
    # given a dictionary of indvidual sentences by MPS, merge those in same party
    byParty = {}

    for mp in byMpDic:
        (name, nameId, party) = mp
        if not party in byParty:
            byParty[party] = []
        byParty[party].extend(byMpDic[mp])
    return byParty

def bowSpeeches(lols):
    # lols is assumed to be a list of lists of strings. Turn into a bow

    bow = {}

    flatList = wNormalisation.flattenList(lols) # becomes a list of strings
    
    for paragraph in flatList:
        #note string might be multiple sentences
        listOfSentences = wNormalisation.sentencesToNormalised(paragraph)
        for sentence in listOfSentences:
            wNormalisation.listToBOW(sentence, bow)

    return bow

def bowByParty(speechByParty):
    ### assumes we have a dictionary with list of lists of strings. want bag of words by party
    output = {}
    for key in speechByParty:
        bow = bowSpeeches(speechByParty[key])
        output[key] = bow
    return output



def produceBowByParty(fileLocation):
    input_file = open(fileLocation)
    byMps = groupByMp(input_file)
    byParty = groupByParty(byMps)
    bowParty = bowByParty(byParty)
    return bowParty


# bow = convertDocument()
# fileLocation = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/2012/2012-06-19.xml"
# produceBowByParty(fileLocation) 