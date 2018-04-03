from unidecode import unidecode
from bs4 import BeautifulSoup
import os
from unidecode import unidecode
import numpy as np
from datetime import datetime



def getRegFrequency(text, regInfos):
    # regInfo must be of from [ [description,regexPattern], ..... [description,regexPattern]]
    output = {}
    


    for description, regPattern in regInfos:


        #print speech
        matches = regPattern.findall(text)
        if matches is None:
            frequency = 0
        else:
            frequency = len(matches)

        if description in output:
            raise ValueError("duplicate description detected : {0}".format(description))
        
        output[description] = frequency
        
        # print description
        # print frequency

        # print text


    return output



def oraganiseByKeyword(dic):
    # dictionary currently in form {date {regex description : value}} want {regex description {date : value}}

    output = {}

    for date in dic:
        for regexDescription in dic[date]:
            if not regexDescription in output:
                output[regexDescription] = {}
            output[regexDescription][date] = dic[date][regexDescription]

    return output


def remove_non_ascii(text):

    #print(text)

    if text:
        return unidecode(text)
    return None


def aggregateByMonth(dic):
    # dic in form of {regex keyword description {date : value}}
    #return dictionary {regex keyword description : array length 12 representing count for each month}
    solution = {}
    
    for regDescription in dic:
        solution[regDescription] = np.zeros([12]).tolist()

    for regDescription in dic:
        for stringDate in dic[regDescription]:
            date = datetime.strptime(stringDate, '%d-%m-%Y')

            month = date.month -1
            #print stringDate
            #print month
            solution[regDescription][month] += dic[regDescription][stringDate]
            # if month < 3 and dic[regDescription][stringDate] > 1:
            #     print month
            #     print dic[regDescription][stringDate]
            #     print solution[regDescription]

    return solution


def aggregateByYear(yearStart, yearEnd, dic):
    # last year not inclusive
    start = int(yearStart)
    end = int(yearEnd)
    solution = {}
    for regDescription in dic:
        #print np.zeros([end-start])
        solution[regDescription] = np.zeros([end-start]).tolist()

    for regDescription in dic:
        for stringDate in dic[regDescription]:
            date = datetime.strptime(stringDate, '%d-%m-%Y')
            yearOffset = date.year - start

            solution[regDescription][yearOffset] += dic[regDescription][stringDate]

    return solution




