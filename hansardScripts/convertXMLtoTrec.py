# converts xml formats to trec

#this supports hansard up to 2014, a differnt script will deal with post then

"""
Example of trec:
<DOC><DOCNO>xxx</DOCNO><DOCHDR>xxx</DOCHDR>texty mc text face </DOC>

"""

import hansardReading

import os
import re
import xml.etree.ElementTree as ET
from unidecode import unidecode


import sys
sys.path.insert(0, '/Users/jeremypattison/LargeDocument/scripts/dataAggregating')
import hansardHandler

outputFolder = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/budgetTrec/"
#outputFolder = /Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/output/

def convert_hansard(folders, reader, withinBudget=False):
	# sort of merge the two prior implementations to just one function for iterating, and two for reading
	for folder in folders:
		input_directory = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/{0}".format(folder)
		output_directory = outputFolder+"{0}".format(folder)
		if not os.path.exists(output_directory):
			os.makedirs(output_directory)

		for filename in os.listdir(input_directory):


			split = str(filename).split('.')
			extension = split[-1].lower()
			if extension != 'xml':
				print split
				continue

			if withinBudget and not hansardHandler.inbetweenDates(filename, True, True):
				continue
			file_path = input_directory+'/'+filename
			input_file = open(file_path)


			id_base = split[0]
			id_sufx = 0
			#print("input path {0}".format(file_path))
			tree = ET.parse(input_file)
			root = tree.getroot()
			output_path = output_directory+'/'+filename+'.trec'
			output_file = open(output_path,'w')

			textArray = reader(root)

			for element in textArray:
				if len(element) <= 0:
					continue
				id_name = "{0}{1}".format(id_base, id_sufx)
				output_file.write("<DOC><DOCNO>"+id_name+"</DOCNO><TEXT>")
				output_file.write(element)
				output_file.write("</TEXT></DOC>")
				id_sufx += 1

			output_file.close()

			input_file.close()

# def convert_hansard_files(files, reader):
# 	# sort of merge the two prior implementations to just one function for iterating, and two for reading
# 	for folder in folders:
# 		output_directory = outputFolder+"{0}".format(folder)
# 		if not os.path.exists(output_directory):
# 			os.makedirs(output_directory)

# 		for filename in os.listdir(input_directory):
# 			split = str(filename).split('.')
# 			extension = split[-1].lower()
# 			if extension != 'xml':
# 				print split
# 				continue

# 			file_path = input_directory+'/'+filename
# 			input_file = open(file_path)


# 			id_base = split[0]
# 			id_sufx = 0
# 			#print("input path {0}".format(file_path))
# 			tree = ET.parse(input_file)
# 			root = tree.getroot()
# 			output_path = output_directory+'/'+filename+'.trec'
# 			output_file = open(output_path,'w')

# 			textArray = reader(root)

# 			for element in textArray:
# 				if len(element) <= 0:
# 					continue
# 				id_name = "{0}{1}".format(id_base, id_sufx)
# 				output_file.write("<DOC><DOCNO>"+id_name+"</DOCNO><TEXT>")
# 				output_file.write(element)
# 				output_file.write("</TEXT></DOC>")
# 				id_sufx += 1

# 			output_file.close()

# 			input_file.close()





# def create_trec_queries(list):
# 	output_directory = "/home/jpattison/ResearchDump/terrier-core-4.2/"
# 	if not os.path.exists(output_directory):
# 		os.makedirs(output_directory)
# 	file = open(output_directory+"query-text.trec",'w')
# 	index = 1
# 	for query in list:
# 		file.write("<top>\n<num>{0}</num><title>\n{1}\n</title>\n</top>\n".format(index,query))
# 		index+=1
# 	file.close()


# queries = ["austerity", "parliament", "marriage", "stop the"]

#getBudgets(years, source, True, True, skipFirstDay = False)


oldFolders = [str(x) for x in range(1998,2011)] 
oldFolders.append('2011_before_april')
newFolders = [str(x) for x in range(2011,2018)] 

# break by paragraph
# convert_hansard(oldFolders, readOldPara)
# convert_hansard(newFolders, readNewPara)

convert_hansard(oldFolders, hansardReading.readOldText, True)
convert_hansard(newFolders, hansardReading.readNewText, True)
