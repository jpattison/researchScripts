"""
The purpose of this is to go through all hansard data and return statistics from it.

1) Read old hansard
2) Build regex counter 
3) create polymorphic oslution for old hansard
4) Same for new
5) Export as JSON
6) Seperate new between question and other time
7) Seperate old

"""

HANSARD_LOCATION = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard"

from unidecode import unidecode


def remove_non_ascii(text):

	#print(text)

	if text:
		return unidecode(text)
	return None



def readOldHansard(yearStart, yearEnd):
	if( yearStart > 2011 or yearstart < 1998):
		raise ValueError("year out of range for readOldHansard")

	
	folders = [str(x) for x in range(yearStart,min(2010,yearEnd))] # note 2011 folder is not called 2011
	if yearEnd == 2011:
		folders.append('2011_before_april') # represents 2011 for old data

	for folder in folders:
		input_directory = HANSARD_LOCATION+"/{0}".format(folder)

		for filename in os.listdir(input_directory):
			file_path = input_directory+'/'+filename
			input_file = open(file_path)

			tree = ET.parse(input_file)
			root = tree.getroot()	
			for para in root.iter('para'):
				print para

readOldHansard(2010,2011)

