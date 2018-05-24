"""
The idea was to compare the transcripts based on the KL of the hansard over same time

How to improve:

1) We probably should normalise by number of transcripts. I.e. average instead of overall
2) We probably want to be selecting specifc parts of hansard rather than the whole thing.


"""
import hansardHandler
import transcriptHandler
import cosineComparison

hansardSource = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalisedStemmed/"

transcriptSource = "/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/budgetBOW" #NOTE GET A STEMMED ONE


initialYear = 2006
finalYear = 2015
_, hansardBows, hansardReference  = hansardHandler.budgetToBow(initialYear, finalYear, None, True, True, False, hansardSource)

#print hansardBows

#print reference

_, transcriptBows, transcriptReference = transcriptHandler.getTranscriptsBudgetDateTechnique(initialYear, finalYear, None, None, 
    transcriptSource, False, False, True)

#print transcriptBows

print transcriptReference

klValues = []
for i in range(len(transcriptBows)):
    klValues.append(cosineComparison.KLbow(hansardBows[i], transcriptBows[i]))


for i in range(len(klValues)):
    print "{0} : {1}".format(transcriptReference[i], klValues[i])