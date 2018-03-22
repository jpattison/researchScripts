from unidecode import unidecode
from bs4 import BeautifulSoup





def remove_non_ascii(text):

	#print(text)

	if text:
		return unidecode(text)
	return None
	#return unidecode(unicode(text, encoding = "utf-8"))

def readTranscript(filename):

	input_file = open(filename)
	soup = BeautifulSoup(input_file, 'html.parser')

	dates = soup.find_all("span", {"class": "data-release-date"})

	speech = soup.find_all("div", {"class": "transcript-body"})
	for thing in dates:
		print thing.text

	for thing in speech:
		print thing
	# root = tree.getroot()


	# for para in root.iter('data-release-date'):


	# 	text = para
	# 	#text = getDebateText('', para)
	# 	#text = re.sub('[\s]+',' ',text)

	# 	ascii_text = remove_non_ascii(text)
	# 	if ascii_text:
	# 		print ascii_text

		


readTranscript('/Users/jeremypattison/LargeDocument/PMSpeeches/xml/transcript-12317')