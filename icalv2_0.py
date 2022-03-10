from mimetypes import init
import pandas as pd
import requests
from Classes import *

# Calcule le temps d'un cours


def lesson_time(event):
    start = event['DTSTART'].dt
    end = event['DTEND'].dt
    time = end - start
    return time.total_seconds() / 3600

# Cette fonction initialise le projet en ouvrant tous les fichiers necessaire


def init():
    pass


def main():
    keywords = ['METHOD', 'PRIDID', 'VERSION', 'CALSCALE',
                'DTSTAMP',  'DTSTART', 'DTEND',
                'SUMMARY',  'LOCATION', 'DESCRIPTION',
                'UID',  'CREATED', 'LAST-MODIFIER ',
                'SEQUECE',  'METHOD', 'PRODID', 'VERSION']
    lexicons = []

    # On ouvre le fichier excel
    labels = pd.read_excel('./DataAnalyse.xlsx')

    # On recupere les calendriers avec l'URL
    url = requests.get("https://ade6-usmb-ro.grenet.fr/jsp/custom/modules/plannings/direct_cal.jsp?data=1b9e1ac2a1720dfd6bd1d42ad86c77f9c55ef35a53135e0070a97be8b09957efa9a0e9cb08b4730b&resources=4586&projectId=3&calType=ical&lastDate=2040-08-14").text

    # On ouvre le fichier .ics
    # file = open('./ADECal.ics', 'r', encoding='utf-8')

    # i = 0
    # while i < len(url):
    for i in range(0, 34):
        c = url[i]
        # print(c)

        keywordFound = False
        theKeyWord = ""
        for keyword in keywords:
            print(url[i:i+len(keyword)])
            if url[i:i+len(keyword)] == keyword:
                lexicons.append(keyword)
                theKeyword = keyword
                keywordFound = True
            if keywordFound:
                i += len(theKeyWord)
            
            # else:
            #     if c == ':':
            #         pass


keys = [
    "METHOD", "PRODID", "VERSION", "CALSCALE", "DTSTAMP", "DTSTART", "DTEND", "SUMMARY",
    "LOCATION", "DESCRIPTION", "UID", "CREATED", "LAST-MODIFIED", "SEQUENCE"
]


CALENDAR = NonTerminal("CALENDAR")
INFOS = NonTerminal("INFOS")
EVENT = NonTerminal("EVENT")
INFODOC = NonTerminal("INFODOC")
INFO = NonTerminal("INFO")
NEXT = NonTerminal("NEXT")

startCal = Terminal("BEGIN:VCALENDAR")
endCal = Terminal("END:VCALENDAR")

startEvent = Terminal("BEGIN:VEVENT")
endEvent = Terminal("END:VEVENT")

key = Terminal("key")
colon = Terminal(":")
data = Terminal("data")

newline = Terminal("\n")

epsilon = Terminal("ε")

grammar = [
    Rule(CALENDAR, [startCal, newline, INFOS, newline, endCal]),

    Rule(INFOS, [EVENT]),
    Rule(INFOS, [INFODOC]),

    Rule(EVENT, [startEvent, INFO, endEvent, NEXT]),
    Rule(EVENT, [epsilon]),

    Rule(INFODOC, [INFO, NEXT]),
    Rule(INFODOC, [epsilon]),

    Rule(NEXT, [INFO, NEXT]),
    Rule(NEXT, [EVENT, NEXT]),
    Rule(NEXT, [epsilon]),

    Rule(INFO, [newline, key, colon, data, newline])
]


if __name__ == '__main__':
    init()
    main()
