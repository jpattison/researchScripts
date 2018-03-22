import numpy as np

import json




def checkAusterity(filename):
	file = open(filename)
	lines = file.readlines()
	austerityCount = 0
	for tweet in lines:
		digital = json.loads(tweet)
		time = digital['created_at']
		text = digital['text']
		if 'austerity' in text:
			austerityCount += 1


	return austerityCount

austCount = []
for day in range(3,7):
	filename = "twitter.2014-06-0{0}-00".format(day)
	print filename
	austCount.append(checkAusterity(filename))
	print austCount