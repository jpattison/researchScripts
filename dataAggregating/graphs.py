
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
    #plt.yticks([2e-2, 2e-1, 2e0])
    #plt.yticks(np.arange(0.05, -2, step=0.2))

    axes = plt.gca()
    axes.set_ylim([-1,0])
    #plt.yscale('log',basey=2) 
    #plt.savefig("/Users/jeremypattison/LargeDocument/graphs/{0}".format(context))
    plt.show()