
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def makeGraph(xAxis, yLabel, title, values, context=None):
    objects = xAxis
    y_pos = np.arange(len(objects))
    performance = values
     
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.yscale('log',basey=2) 

    #plt.yticks([2e-2, 2e-1, 2e0])
    #plt.yticks(np.arange(0.05, -2, step=0.2))

    axes = plt.gca()
    #axes.set_ylim([0,1])

    axes.set_ylim([2**-2,1])

    #plt.savefig("/Users/jeremypattison/LargeDocument/graphs/{0}".format(context))
    plt.show()


def setSubplots(xAxes, yLabels, title, yValues):

    n = len(xAxes)
    plt.title(title)

    for i in range(n):
        plt.subplot(n, 1, i+1)
        #print xAxes[i]
        plt.bar(xAxes[i], yValues[i])
        plt.ylabel(yLabels[i])
        axes = plt.gca()
        axes.set_ylim([0,0.8])
    plt.subplots_adjust(hspace=0.4)
    plt.show()