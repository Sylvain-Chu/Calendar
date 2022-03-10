from __future__ import print_function
from asyncio.windows_events import NULL
from importlib.resources import contents
from tabnanny import check
import pandas as pd
import requests
from Classes import *


def init():
    pass


def main():

    # On ouvre le fichier excel
    labels = pd.read_excel('./DataAnalyse.xlsx')

    # On recupere les calendriers avec l'URL
    url = requests.get("https://ade6-usmb-ro.grenet.fr/jsp/custom/modules/plannings/direct_cal.jsp?data=1b9e1ac2a1720dfd6bd1d42ad86c77f9c55ef35a53135e0070a97be8b09957efa9a0e9cb08b4730b&resources=4586&projectId=3&calType=ical&lastDate=2040-08-14").text

    trigger = {
        'startCalendar': 'BEGIN:VCALENDAR',
        'endCalendar': 'END:VCALENDAR',
        'startEvent': 'BEGIN',
        'endEvent': 'END'
    }

    keywords = ['BEGIN', 'METHOD', 'PRODID', 'VERSION',
                'CALSCALE', 'DTSTAMP', 'DTSTART', 'DTEND', 'SUMMARY',
                'LOCATION', 'DESCRIPTION', 'UID', 'CREATED', 'LAST-MODIFIED',
                'SEQUENCE', 'END']

    newline = ["\n"]
    separator = [":"]
    lexicons = []

    i = 0
    for i in range(0, url.__sizeof__()-75):
        c = url[i]
        keywordFound = False
        theKeyWord = ""
        for keyword in keywords:
            if url[i:i+len(keyword)] == keyword:
                theKeyword = keyword
                keywordFound = True

            if keywordFound:
                i += len(theKeyWord)

            data = ""
            if c in separator:
                while c not in newline:
                    i += 1
                    c = url[i]
                    data += c
                lexicons.append([theKeyword, data])

    for x in lexicons:
        x[1] = x[1].replace("\r", '')
        x[1] = x[1].replace("\n", '')

    c = Calendar(lexicons[1][1], lexicons[2][1],
                 lexicons[3][1], lexicons[4][1])

    lexicons.pop(4)
    lexicons.pop(3)
    lexicons.pop(2)
    lexicons.pop(1)
    lexicons.pop(0)

    events = []
    for i in lexicons:
        print(i)
        if i[0] == trigger['startEvent']:
            e = Event()
        elif e != NULL:
            match i[0]:
                case 'DTSTAMP':
                    e.dtstamp = i[1]
                case 'DTSTART':
                    e.dtstart = i[1]
                case 'DTEND':
                    e.dtend = i[1]
                case 'SUMMARY':
                    e.sumary = i[1]
                case 'LOCATION':
                    e.location = i[1]
                    flag = True
                case 'DESCRIPTION':
                    if flag == True:
                        e.description = i[1]
                        flag = False
                case 'UID':
                    e.uid = i[1]
                case 'CREATED':
                    e.created = i[1]
                case 'LAST-MODIFIED':
                    e.lastmodified = i[1]
                case 'SEQUENCE':
                    e.sequence = i[1]
                case 'END':
                    events.append(e)
    c.events = events


if __name__ == '__main__':
    init()
    main()