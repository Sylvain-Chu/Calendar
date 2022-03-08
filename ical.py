import datetime
from mimetypes import init
import numpy as np
import pandas as pd
import icalendar as ic
import matplotlib.pyplot as plt
from datetime import timedelta
from tkinter import *

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
    labels = pd.read_excel('./DataAnalyse.xlsx')

    # On ouvre le fichier .ics
    file = open('./ADECal.ics', 'r', encoding='utf-8')
    cal = ic.Calendar.from_ical(file.read())

    # On met le fichier excel sous forme de matrice
    data = pd.DataFrame(np.zeros((labels.shape[0], labels.shape[1])))
    data.columns = labels.columns

    # dataframe = pd.DataFrame({'Matière': [],
    #                           'Description': [],
    #                           'Heure de début': [],
    #                           'Heure de fin': []})

    # dataframe.to_excel('DataAnalyse.xlsx')
    
    # On parcours tous les evenements du fichier ical
    for event in cal.walk('vevent'):
        time = lesson_time(event)
        summary = str(event.get('summary'))
        desc = str(event.get('description'))
        start = str(event.get('dtstart'))
        end = str(event.get('dtend'))

        
        for i in range(0, labels.shape[0]):
            for j in range(0, labels.shape[1]):
                pass


if __name__ == '__main__':
    init()
    main()
