import xml.etree.ElementTree as ET
import re

def getDebateText(current, element):
	if element.text is not None:
		current = current + element.text
	for child in element:
		current = getDebateText(current, child



			)
	return current

file = open("/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/2012/2012-02-07.xml")

tree = ET.parse(file)

root = tree.getroot()

for para in root.iter('talk.text'):
		
		text = getDebateText('', para)
		text = re.sub('[\s]+',' ',text)



