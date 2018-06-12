
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import matplotlib.dates as mdates
def makeGraph(xAxis, yLabel, title, values, context=None):
    objects = xAxis
    y_pos = np.arange(len(objects))
    performance = values
     
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(yLabel)
    plt.title(title)
    #plt.yscale('log',basey=2) 

    #plt.yticks([2e-2, 2e-1, 2e0])
    #plt.yticks(np.arange(0.05, -2, step=0.2))


    axes = plt.gca()
    #axes.set_ylim([0,1])

    #axes.set_ylim([2**-4,1])

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
        axes.set_ylim([0,0.3])
    plt.subplots_adjust(hspace=0.4)
    plt.show()


def lineOverTime(xAxis, yLabel, title, values) :

    # this is a very crude print out line graph over time
    # xAxis is a list of dates (in datetime)
    # values is the yValues
    # we're not actually using yLabel / title yet. Probably should

    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')


    fig, ax = plt.subplots()
    ax.plot(xAxis, values)


    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    #ax.title(title)
    datemin = xAxis[0] #xAxis[0].year
    datemax = xAxis[-1] #.year + 1

    ax.set_xlim(datemin, datemax)
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.grid(True)
    
    fig.autofmt_xdate()

    plt.show()
