import re
import os

import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py






directory = '/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/output/'

austerity = []
budget = []
names = []


for folder in os.listdir(directory):
	#print folder
	folderYear = directory+folder+'/'
	


for subdir, dirs, files in os.walk(directory):
	for file in files:
		filepath = os.path.join(subdir, file)

		if not file.endswith(".trec"):
			continue
		names.append(file)
		text = open(filepath).readlines()
		austerity_count = 0
		budget_count = 0
		for line in text:
			austerity_count += len(re.findall("[Aa]uster\w*", line))
			#budget_count += len(re.findall("[Bb]udget\w*", line))
		austerity.append(austerity_count)
		budget.append(budget_count)
#print budget
print len(austerity)
print len(names)
print austerity
x_axis = x = np.arange(0, 400)

print x_axis


plt.plot(x_axis, austerity, 'k-')
plt.plot(x_axis, budget, 'y-')
plt.show()

