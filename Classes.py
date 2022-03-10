from datetime import datetime


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

class Calendar:
	# def __init__(self, event):
	# 	self.event = event

    def __init__(self, method, prodid, version, calscale):
        self.method = method
        self.prodid = prodid
        self.version = version
        self.calscale = calscale
        self.event = []



class Event:
    def __init__(self, dtstart, dtend, sumary, location, description, uid, created, lastmodified, sequence):
        self.dtstamp = datetime.now()
        self.dtstart = dtstart
        self.dtend = dtend
        self.sumary = sumary
        self.location = location
        self.description = description
        self.uid = uid
        self.created = created
        self.lastmodified = lastmodified
        self.sequence = sequence

    def __init__(self):
        self.dtstamp = datetime.now()
