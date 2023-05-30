from datetime import datetime

# Entry model definition with default entrytime set to datetime.now()
# The entry is the fundamental unit of the guestbook.
# This model should simply reflect what an entry is from the database point of view


class Entry:
    def __init__(self, firstname, lastname, message, entrytime=None):
        self.firstname = firstname
        self.lastname = lastname
        self.message = message
        self.entrytime = entrytime or datetime.utcnow()
