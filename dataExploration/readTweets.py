import numpy as np

import json
import re
import os



def checkKeyCount(filename, keyword):
	# this just returns number of tweets with keyword in it. Not number times mentioned
	print filename
	file = open(filename)
	lines = file.readlines()
	key_count = 0
	for tweet in lines:
		#print tweet
		digital = json.loads(tweet)
		time = digital['created_at']
		text = digital['text']
		if keyword in text.lower():
			key_count += 1


	return key_count

# austCount = []
# for day in range(3,7):
# 	filename = "twitter.2014-06-0{0}-00".format(day)
# 	print filename
# 	austCount.append(checkAusterity(filename))
# 	print austCount

def readTweets(inputDirectory):
	p = re.compile('\d{4}-\d{2}-\d{2}')
	counts = {}
	for filename in os.listdir(inputDirectory):
		filePath = inputDirectory+'/'+filename
		dates = p.findall(filename)

		if dates is None or dates == []:
			#print filename
			#print p.match(filename)
			continue
		date = dates[0]
		if date not in counts:
			counts[date]=0
		counts[date]+=checkKeyCount(filePath, 'austerity')
	print counts


readTweets('/Users/jeremypattison/LargeDocument/twitter/tcohn')

