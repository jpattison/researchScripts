"""
The idea was to compare the transcripts based on the KL of the hansard over same time

How to improve:

1) We probably should normalise by number of transcripts. I.e. average instead of overall
2) We probably want to be selecting specifc parts of hansard rather than the whole thing.


"""
import hansardHandler
import transcriptHandler
import cosineComparison
import graphs
#hansardSource = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalisedStemmed/"
#hansardSource = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalisedStemmed/"
hansardSource = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/byParty/bowNormalisedAndStemmed/"

transcriptSource = "/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/bowNormalisedStemmed"


initialYear = 2008
finalYear = 2015

partyFunction = hansardHandler.filenameToPartyInCharge


_, hansardBows, hansardReference  = hansardHandler.budgetToBow(initialYear, finalYear, None, partyFunction, True, True, False, hansardSource)

#print hansardBows

#print reference

_, transcriptBows, transcriptReference = transcriptHandler.getTranscriptsBudgetDateTechnique(initialYear, finalYear, None, None, 
    transcriptSource, False, False, True)

#print transcriptBows

#print transcriptReference

klValues = []
xAxis = []
for i in range(len(transcriptBows)):
    klValues.append(cosineComparison.KLbow(hansardBows[i], transcriptBows[i]))

print klValues
for i in range(len(klValues)):
    print "{0} : {1}".format(transcriptReference[i], klValues[i])
    xAxis.append(transcriptReference[i])

#xAxis = [pair[0] for pair in transcriptReference[i]]

graphs.makeGraph(xAxis, "scores", "KlHansardTranscripts", klValues)