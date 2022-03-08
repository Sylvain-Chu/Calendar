from ast import keyword
import datetime
from hashlib import new
from lib2to3.pgen2 import grammar
from mimetypes import init
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
from tkinter import *
from pyparsing import col
import requests

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
    keywords = ['BEGIN', 'END', 'DTSTART', 'DTEND',
                'SUMMARY',  'LOCATION', 'DESCRIPTION']
    lexicons = []

    # On ouvre le fichier excel
    labels = pd.read_excel('./DataAnalyse.xlsx')

    # On recupere les calendriers avec l'URL
    url = requests.get("https://ade6-usmb-ro.grenet.fr/jsp/custom/modules/plannings/direct_cal.jsp?data=1b9e1ac2a1720dfd6bd1d42ad86c77f9c55ef35a53135e0070a97be8b09957efa9a0e9cb08b4730b&resources=4586&projectId=3&calType=ical&lastDate=2040-08-14").text

    # On ouvre le fichier .ics
    # file = open('./ADECal.ics', 'r', encoding='utf-8')

    i = 0
    for i in range(0, 500):
        c = url[i]

        keywordFound = False
        theKeyWord = ""
        for keyword in keywords:
            if url[i:i+len(keyword)] == keyword:
                lexicons.append(keyword)
                theKeyword = keyword
                keywordFound = True
            if keywordFound:
                i += len(theKeyWord)


class Tree:
    """ un symbole (générique) et un ensemble d'enfants """

    def __init__(self, symbol):
        self.symbol = symbol
        self.nodes = []
    """ affichage indenté """

    def __str__(self):
        return self.__strIndent__(0)

    """ ajouter un enfant (raccourci) """

    def add(self, symbol):
        self.nodes.append(Tree(symbol))

    """ sélection d'un noeud en fonction du symbole (récursivement) """

    def select(self, symbol):
        if self.symbol == symbol:
            return self
        for node in self.nodes:
            sub = node.select(symbol)
            if sub != None:
                return sub
        return None

    """ liste de tous les noeuds en parcours récursif (parent d'abord) """

    def asList(self):
        if len(self.nodes) == 0:
            return [self]
        else:
            list = [self]
            for node in self.nodes:
                list.extend(node.asList())
            return list

    """ noeud suivant d'un noeud dans le parcours récursif. Fonction bourrine à optimiser ! """

    def nextNode(self, node):
        list = self.asList()
        for i in range(len(list)):
            if list[i] == node and i < len(list)-1:
                return list[i+1]
        return None


class Symbol:
    def __init__(self, word):
        self.word = word

    def __str__(self):
        return self.word


class Terminal(Symbol):
    pass


class NonTerminal(Symbol):
    pass


class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        s = str(self.left) + " -> "
        for sym in self.right:
            s += str(sym) + " "
        return s

keys = [
	"METHOD", "PRODID", "VERSION", "CALSCALE", "DTSTAMP", "DTSTART", "DTEND", "SUMMARY", 
    "LOCATION", "DESCRIPTION", "UID", "CREATED", "LAST-MODIFIED", "SEQUENCE"
]


CALENDAR = NonTerminal("CALENDAR")
INFOS = NonTerminal("INFOS")
EVENT = NonTerminal("EVENT")
INFODOC = NonTerminal("INFODOC")
INFO = NonTerminal("INFO")

startCal = Terminal("BEGIN:VCALENDAR")
endCal = Terminal("END:VCALENDAR")

startEvent = Terminal("BEGIN:VEVENT")
endEvent = Terminal("END:VEVENT")

key = Terminal("key")
colon = Terminal(":")
data = Terminal("data")

newline = Terminal("\n")

grammar = [
    Rule(CALENDAR, [startCal, newline, INFOS, newline, endCal]),
    Rule(INFOS, [EVENT]),
    Rule(INFOS, [INFODOC]),
    
    Rule(EVENT, [startEvent, INFO, endEvent, EVENT]),
    Rule(EVENT, [startEvent, INFO, endEvent]),
    
    Rule(INFODOC, [INFO, INFO]),
    Rule(INFODOC, [INFO]),
    
    Rule(INFO, [newline, key, colon, data, newline])
]



if __name__ == '__main__':
    init()
    main()