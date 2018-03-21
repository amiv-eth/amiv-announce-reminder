from datetime import datetime


# NETHZ Credentials
USER = ''
PASSWORD = ''

# Name of the Infovorstand
INFOVORSTAND_FIRST_NAME = ''
INFOVORSTAND_LAST_NAME = ''

# Deadline (e.g. 20:00)
DEADLINE_TIME = datetime.strptime('20:00', '%H:%M').time()

# How many days after the reminder is the deadline?
DAYS_REMINDER_DEADLINE = 4

# How many days after the deadline is the Announce sent?
DAYS_DEADLINE_ANNOUNCE = 1
