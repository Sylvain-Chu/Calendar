from datetime import date


class Event:
    def __init__(self, dtstamp, dtstart, dtend, sumary, location, description, uid, created, lastmodified, sequence):
        self.dtstamp = dtstamp
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
        self.description = 'e'
