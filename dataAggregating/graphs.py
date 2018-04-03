import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

import json


def makeGraph(xAxis, yLabel, title, values):
    objects = xAxis
    y_pos = np.arange(len(objects))
    performance = values
     
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(yLabel)
    plt.title(title)
     
    plt.show()



file = open('hanByMonth.json', 'r')

dic = json.loads(file.readline())

for regExpression in dic:
    print regExpression
    print dic[regExpression]
    makeGraph(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], "amount", regExpression, dic[regExpression])


file = open('hanByYear.json', 'r')

dic = json.loads(file.readline())


years = ["2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"]


for regExpression in dic:
    print regExpression
    print dic[regExpression]
    makeGraph(years, "amount", regExpression, dic[regExpression])



print "now prime minister"

file = open('pmByMonth.json', 'r')

dic = json.loads(file.readline())

for regExpression in dic:
    print regExpression
    print dic[regExpression]
    makeGraph(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], "amount", regExpression, dic[regExpression])


file = open('pmByYear.json', 'r')

dic = json.loads(file.readline())

for regExpression in dic:
    print regExpression
    print dic[regExpression]
    makeGraph(years, "amount", regExpression, dic[regExpression])

