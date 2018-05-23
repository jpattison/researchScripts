"""
The idea was to compare the transcripts based on the KL of the hansard over same time

Plan: 1) Do it for one year. Call the hansard to get the budget of that year. Call the transcripts. 
Then use the hansard as the base and measure cross entropy



"""
import hansardHandler
import transcriptHandler

hansardSource = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/bowNormalisedStemmed/"

transcriptSource = "/Users/jeremypattison/LargeDocument/ResearchProjectData/PMSpeeches/budgetBOW" #NOTE GET A STEMMED ONE


initialYear = 2010
finalYear = 2012
_, hansardBows, hansardReference  = hansardHandler.budgetToBow(initialYear, finalYear, None, True, True, False, hansardSource)

#print hansardBows

#print reference

_, transcriptBows, transcriptReference = transcriptHandler.getTranscriptsBudgetDateTechnique(initialYear, finalYear, None, None, 
    transcriptSource, False, False, True)

print transcriptBows

print transcriptReference

