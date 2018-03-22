# converts xml formats to trec

#this supports hansard up to 2014, a differnt script will deal with post then

"""
Example of trec:
<DOC><DOCNO>xxx</DOCNO><DOCHDR>xxx</DOCHDR>texty mc text face </DOC>

"""

import os
import re

import xml.etree.ElementTree as ET
from unidecode import unidecode

def remove_non_ascii(text):

	#print(text)

	if text:
		return unidecode(text)
	return None
	#return unidecode(unicode(text, encoding = "utf-8"))


#directory = os.getcwd()

def getDebateText(current, element):
	if element.text is not None:
		current = current + element.text
	for child in element:
		current = getDebateText(current, child)
	return current


def convert_old_hansard():
	folders = [str(x) for x in range(1998,2011)] 
	folders.append('2011_before_april')

	for folder in folders:
		input_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/{0}".format(folder)
		output_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/output/{0}".format(folder)
		if not os.path.exists(output_directory):
			os.makedirs(output_directory)

		for filename in os.listdir(input_directory):
			file_path = input_directory+'/'+filename
			input_file = open(file_path)


			id = 0
			#print("input path {0}".format(file_path))
			tree = ET.parse(input_file)
			root = tree.getroot()
			output_path = output_directory+'/'+filename+'.trec'
			output_file = open(output_path,'w')			


			for para in root.iter('para'):
				name = filename+"-{0}".format(id)

				#print("output file: {0}".format(output_path))
				#print("para start: \n")
				ascii_text = remove_non_ascii(para.text)
				if ascii_text:
					output_file.write("<DOC><DOCNO>"+name+"</DOCNO><TEXT>")
					output_file.write(ascii_text)

					#print(ascii_text)
					#print("para end: \n \n")
					output_file.write("</TEXT></DOC>")

				id+=1

				# we probably want to split it up
			output_file.close()

			input_file.close()


def convert_new_hansard():
	folders = [str(x) for x in range(2011,2018)] 

	for folder in folders:
		input_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/{0}".format(folder)
		output_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/output/{0}".format(folder)
		if not os.path.exists(output_directory):
			os.makedirs(output_directory)

		for filename in os.listdir(input_directory):

			extension = str(filename).split('.')[-1].lower()
			if extension != 'xml':
				continue
			file_path = input_directory+'/'+filename
			input_file = open(file_path)

			id = 0
			#print("input path {0}".format(file_path))
			print input_file
			tree = ET.parse(input_file)
			root = tree.getroot()
			output_path = output_directory+'/'+filename+'.trec'
			output_file = open(output_path,'w')			


			for para in root.iter('talk.text'):
				name = filename+"-{0}".format(id)

				#print("output file: {0}".format(output_path))
				#print("para start: \n")
				
				text = getDebateText('', para)
				text = re.sub('[\s]+',' ',text)

				ascii_text = remove_non_ascii(text)
				if ascii_text:
					output_file.write("<DOC><DOCNO>"+name+"</DOCNO><TEXT>")
					output_file.write(ascii_text)

					#print(ascii_text)
					#print("para end: \n \n")
					output_file.write("</TEXT></DOC>")

				id+=1

				# we probably want to split it up
			output_file.close()

			input_file.close()





def create_trec_queries(list):
	output_directory = "/home/jpattison/ResearchDump/terrier-core-4.2/"
	if not os.path.exists(output_directory):
		os.makedirs(output_directory)
	file = open(output_directory+"query-text.trec",'w')
	index = 1
	for query in list:
		file.write("<top>\n<num>{0}</num><title>\n{1}\n</title>\n</top>\n".format(index,query))
		index+=1
	file.close()


queries = ["austerity", "parliament", "marriage", "stop the"]

#convert_old_hansard()	
#create_trec_queries(queries)
convert_new_hansard()
