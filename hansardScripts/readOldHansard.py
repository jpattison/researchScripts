"""

Idea is to group speeches by a minister. Preferably by a party. Idea is follow format of readNewHansard

word normalisation to be done by hansardReading


structure looking at:

<TYPEOFTALK> <talk.start> <talker> usefule information </talker </talk.start> <BLOCKX> <para> text </para> (repeat) </BLOCKX> <para> text </para> (repeat)

TYPEOFTALK : [speech, question, answer]

BLOCKX can be [motion, quote, other]

My idea is to recursively get text from para whenever block encounted

Bad blocks are:
[interjection, 


TODO:
0) merge with readNew?
1) Remove stuff from speaker
2) Theres a lot of inline stuff that will likely lead to things skipped
3) Might need to double check the things im skipping.
4) We have noticed quite a few incorreclty labelled speeches, this poses a problem if we overwrite a person if half their information is one person and other 
 see id YU5 in 30th march 1998

Special notes:
1) Have removed interjections


"""


import xml.etree.ElementTree as ET
import wNormalisation
import re


def readTalk(talk):
    # associates the speaker with the text.

    typeSpeech = talk.tag
    if typeSpeech in ["interjection", "petition", "presenter"]:
        return None
    talkDic = {}

    talkStart = talk.find("./talk.start")


    getTalkDetails(talkDic, talkStart)
    getTalkText(talkDic, talk)

    return talkDic


def getTalkDetails(talkDic, talkStart):
    # Grab all attributes about the speaker
    # There's actually more generally in the poorly formatted below but this generally gets name/party
    talker = talkStart.find("./talker")
    for child in talker:
        talkDic[child.tag] = child.text

def getTalkText(talkDic, talkText):
    # note this is noticebly differnt from readNewHansard
    speech = []
    immediateParagraphs = talkText.findall("./para")
    subParagraphs = talkText.findall("*/para") # only want one level down

    for subelement in immediateParagraphs:
        speech.append(subelement.text)
    for subelement in subParagraphs:
        speech.append(subelement.text)

    normalisedSpeech = wNormalisation.normaliseText(speech)
    talkDic["speech"] = normalisedSpeech


def findNameId(individualSpeech, overallDic):
    # sometimes we're given a name not an id
    if "name.id" in individualSpeech:
        return individualSpeech["name.id"]
    elif "name" in individualSpeech:
        individualName = individualSpeech["name"]
        for mpId in overallDic:
            if "name" in overallDic[mpId]["person"]:
                mpName = overallDic[mpId]["person"]["name"]
                if individualName == mpName:
                    nameId = mpId
                    print "fixed absent id"
                    return nameId
    else:
        return None


def attatchSpeechToMp(overallDic, individualSpeech):
    nameId = findNameId(individualSpeech, overallDic)

    if not nameId:
        print "no id found"
        return
    # if not (name, nameId, party) in overallDic:
    #     overallDic[(name, nameId, party)] = []

    if not nameId in overallDic:
        overallDic[nameId] = {"person": {}, "speech": []}
    
    attributes = individualSpeech.keys()
    if "speech" in attributes:
        attributes.remove("speech")

    #print attributes
    for attribute in attributes:
        if attribute not in overallDic[nameId]["person"]:
            overallDic[nameId]["person"][attribute] = individualSpeech[attribute]


    overallDic[nameId]["speech"].append(individualSpeech["speech"])


### anything below is pretty much copy pasted so should aim to merge in


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

    for nameId in byMpDic:
        nameId = fixNameId(nameId, byMpDic)
        if nameId in ["YU5", "10000"] and not "party" in byMpDic[nameId]["person"]:
            print "skipped " + nameId
            continue

        elif not "party" in byMpDic[nameId]["person"]:
            print "This person gonna break something"
            print byMpDic[nameId]["person"]
            continue
        party = byMpDic[nameId]["person"]["party"]
        if not party in byParty:
            byParty[party] = []
        byParty[party].extend(byMpDic[nameId]["speech"])
    return byParty

def bowSpeeches(lols, removeCapitals, stemWords):
    # lols is assumed to be a list of lists of strings. Turn into a bow

    bow = {}

    flatList = wNormalisation.flattenList(lols) # becomes a list of strings
    
    for paragraph in flatList:
        #note string might be multiple sentences
        listOfSentences = wNormalisation.sentencesToNormalised(paragraph, removeCapitals, stemWords)
        for sentence in listOfSentences:
            wNormalisation.listToBOW(sentence, bow)

    return bow

def bowByParty(speechByParty, removeCapitals, stemWords):
    ### assumes we have a dictionary with list of lists of strings. want bag of words by party
    output = {}
    for key in speechByParty:
        bow = bowSpeeches(speechByParty[key], removeCapitals, stemWords)
        output[key] = bow
    return output



def produceBowByParty(fileLocation, removeCapitals, stemWords):
    input_file = open(fileLocation)
    byMps = groupByMp(input_file)
    byParty = groupByParty(byMps)
    bowParty = bowByParty(byParty, removeCapitals, stemWords)
    return bowParty   


def fixNameId(nameId, byMpDic):
    # if we've been given a nameId that doesn't match to anyone
    if "party" in byMpDic[nameId]["person"]:
        return nameId
    # assume party isn't there. Might be misaligned id.
    if "name" in byMpDic[nameId]["person"]:
        name = byMpDic[nameId]["person"]["name"]
        for mpId in byMpDic:
            if "name" in byMpDic[mpId]["person"] and "party" in byMpDic[mpId]["person"]:
                mpName = byMpDic[mpId]["person"]["name"]

                if name == mpName:
                    nameId = mpId
                    return nameId
    return nameId



# fileLocation = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/1999/1999-06-22.xml"
# print produceBowByParty(fileLocation)



