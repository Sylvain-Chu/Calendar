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

    print(url.__sizeof__())



    trigger = {
        'startCalendar': 'BEGIN:VCALENDAR',
        'endCalendar': 'END:VCALENDAR',
        'startEvent': 'BEGIN:VEVENT',
        'endEvent': 'END:VEVENT'
    }

    keywords = ['BEGIN', 'METHOD', 'PRODID', 'VERSION',     
                'CALSCALE', 'DTSTAMP', 'DTSTART', 'DTEND','SUMMARY',
                'LOCATION', 'DESCRIPTION', 'UID','CREATED', 'LAST-MODIFIED',
                'SEQUENCE']

    newline = ["\n"]
    separator = [":"]
    lexicons = []

    i = 0
    for i in range(0, url.__sizeof__()-75):
        c = url[i]   
        print(c)     
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
                lexicons.append([theKeyword,data])

    for x in lexicons:        
        x[1] = x[1].replace("\r", '')
        x[1] = x[1].replace("\n", '')

    
    c = Calendar(lexicons[1][1], lexicons[2][1], lexicons[3][1], lexicons[4][1])
    
    
    lexicons.pop(4)
    lexicons.pop(3)
    lexicons.pop(2)
    lexicons.pop(1)  
    lexicons.pop(0)
    
    # print(lexicons)
    

    


if __name__ == '__main__':
    init()
    main()