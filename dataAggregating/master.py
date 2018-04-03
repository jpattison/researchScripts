import keywordPM as kP
import keywordHansard as kH
import freq
import re
import json

ecoDescription = "economy"
ecoRegex = re.compile('[Ee]conomy')

ausDescription = "checking for austerity"
ausRegex = re.compile('[Aa]usterity')

budDescription = "checking for budget"
budRegex = re.compile('[Bb]udget')

budCutDescription = "checking for budget cuts"
budCutRegex = re.compile('[Bb]udget.{0,20}cut')

regList = [[ecoDescription, ecoRegex], [ausDescription, ausRegex], [budDescription, budRegex], [budCutDescription, budCutRegex]]

yearStart = "2003"

yearEnd = "2016"

hansardRawFreq = kH.readHansard(yearStart, yearEnd, kH.oldReader, kH.newReader, freq.getRegFrequency, regList)

#print hansardRawFreq

hanOrganised = freq.oraganiseByKeyword(hansardRawFreq)

#print hanOrganised




hanByMonth = freq.aggregateByMonth(hanOrganised)

with open('hanByMonth.json', 'w') as fp:
    json.dump(hanByMonth, fp)

hanByYear = freq.aggregateByYear(yearStart, yearEnd, hanOrganised)

with open('hanByYear.json', 'w') as fp:
    json.dump(hanByYear, fp)    

print "done hansard"

pmRawFreq = kP.readTranscripts(yearStart, yearEnd, kP.getTranscript ,freq.getRegFrequency, regList)

pmOrganised = freq.oraganiseByKeyword(pmRawFreq)

pmByMonth = freq.aggregateByMonth(pmOrganised)

with open('pmByMonth.json', 'w') as fp:
    json.dump(pmByMonth, fp)


pmByYear = freq.aggregateByYear(yearStart, yearEnd, pmOrganised)

with open('pmByYear.json', 'w') as fp:
    json.dump(pmByYear, fp)

