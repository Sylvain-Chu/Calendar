from asyncio.windows_events import NULL
import requests
from Classes import *
import datetime
import csv
import xlsxwriter


def init():
    global url
    global labels
    global trigger
    global keywords
    global workbook

    # On recupere les calendriers avec l'URL
    url = requests.get("https://ade6-usmb-ro.grenet.fr/jsp/custom/modules/plannings/direct_cal.jsp?data=1b9e1ac2a1720dfd6bd1d42ad86c77f9c55ef35a53135e0070a97be8b09957efa9a0e9cb08b4730b&resources=4586&projectId=3&calType=ical&lastDate=2040-08-14").text
    # On ouvre le fichier excel
    workbook = xlsxwriter.Workbook('DataAnalyse.xlsx')

    trigger = {
        'startCalendar': 'BEGIN:VCALENDAR',
        'endCalendar': 'END:VCALENDAR',
        'startEvent': 'BEGIN',
        'endEvent': 'END'
    }

    keywords = ['BEGIN', 'METHOD', 'PRODID', 'VERSION',
                'CALSCALE', 'DTENDDTSTAMP', 'DTSTART', 'DTSTAMP', 'SUMMARY',
                'LOCATION', 'DESCRIPTION', 'UID', 'CREATED', 'LAST-MODIFIED',
                'SEQUENCE', 'END']


def create_Calendar():
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
                # print(url[i:i+len(keyword)])

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

    global cal
    cal = Calendar(lexicons[1][1], lexicons[2][1],
                   lexicons[3][1], lexicons[4][1])

    lexicons.pop(4)
    lexicons.pop(3)
    lexicons.pop(2)
    lexicons.pop(1)
    lexicons.pop(0)
    lexicons.pop()

    events = []
    for i in lexicons:
        if i[0] == trigger['startEvent']:
            e = Event()
        elif e != NULL:
            match i[0]:
                case 'DTSTAMP':
                    e.dtstamp = i[1]
                case 'DTSTART':
                    e.dtstart = datetime.datetime.strptime(
                        i[1], '%Y%m%dT%H%M%SZ')
                case 'END':
                    if(i[1] == 'VEVENT'):
                        events.append(e)
                    else:
                        e.dtend = datetime.datetime.strptime(
                            i[1], '%Y%m%dT%H%M%SZ')
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

    cal.events = events


def create_excel(cal):

    columns = ['Matière', 'Salle', 'Description',
               'Date de début', 'Date de fin', 'Durée']


    worksheet = workbook.add_worksheet()

    row = 0
    column = 0

    for col in columns:
        worksheet.write(row, column, col)
        column += 1
        
    row += 1   
    column = 0

    formatdate = workbook.add_format({'num_format': 'dd/mm/yy'})
    formatheure = workbook.add_format({'num_format': 'hh:mm:ss'})


    for e in cal.events:
        column = 0
        
        worksheet.write(row, column, e.sumary)
        column += 1
        worksheet.write(row, column, e.location)
        column += 1
        worksheet.write(row, column, e.description)
        column += 1
        worksheet.write(row, column, e.dtstart, formatdate)
        column += 1
        worksheet.write(row, column, e.dtend, formatdate)
        column += 1
        worksheet.write(row, column, lesson_time(e), formatheure)
        column += 1
        row += 1

    workbook.close()


def lesson_time(e):
    time = e.dtend - e.dtstart
    return time


if __name__ == '__main__':
    init()
    create_Calendar()
    create_excel(cal)
