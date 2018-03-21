#!/bin/env python3
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText
import locale
from smtplib import SMTP
import sys

from config import (USER,
                    PASSWORD,
                    INFOVORSTAND_FIRST_NAME,
                    INFOVORSTAND_LAST_NAME,
                    DEADLINE_TIME,
                    DAYS_REMINDER_DEADLINE,
                    DAYS_DEADLINE_ANNOUNCE)


TESTING = not (len(sys.argv) > 1 and sys.argv[1] == '--notest')
FROM_ADDR = 'info@amiv.ethz.ch'
TO_ADDRS = ['vorstand@amiv.ethz.ch',
            'kommissionen@amiv.ethz.ch'] if not TESTING else ['info@amiv.ethz.ch']


def send_reminder(announce_date, deadline):
    """Send reminder e-mail."""
    # Construct message
    msg_content = '''Hallo zusammen,<br>
                    <br>
                    die nächste Announce erscheint am {announce_date}. Bitte schickt mir eure Beiträge bis am <b>{deadline}</b>.<br>
                    <br>
                    Liebe Grüsse<br>
                    {infovorstand_first_name}
                    '''.format(announce_date=announce_date,
                               deadline=deadline,
                               infovorstand_first_name=INFOVORSTAND_FIRST_NAME)
    message = MIMEText(msg_content, 'html')

    # Send headers
    message['From'] = '{first_name} {last_name} <{email}>'.format(first_name=INFOVORSTAND_FIRST_NAME,
                                                                  last_name=INFOVORSTAND_LAST_NAME,
                                                                  email=FROM_ADDR)
    message['To'] = ', '.join(['<{}>'.format(rec) for rec in TO_ADDRS])
    message['Subject'] = 'Einsendeschluss Announce vom {announce_date}'.format(announce_date=announce_date)

    with SMTP('smtp.ee.ethz.ch', port=587) as smtp:
        # Open connection to mail server
        smtp.starttls()
        smtp.ehlo()

        # log in
        smtp.login(USER, PASSWORD)

        # send e-mail
        smtp.sendmail(from_addr=FROM_ADDR,
                      to_addrs=TO_ADDRS,
                      msg=message.as_string())

        # close connection
        smtp.quit()


def main():
    """The main function."""
    # Set locale
    locale.setlocale(locale.LC_ALL, '')

    # Read 'reminder days'
    with open('reminder_day.txt') as reminder_file:
        REMINDER_DAYS = reminder_file.readlines()
    
    # Strip whitespace
    REMINDER_DAYS = [reminder_day.strip() for reminder_day in REMINDER_DAYS]

    # Check if today is a reminder day
    TODAY = date.today()
    for reminder_day in REMINDER_DAYS:
        # Skip blank lines
        if not reminder_day:
            continue

        if TODAY == datetime.strptime(reminder_day, '%d.%m.%Y').date():
            # Calculate relevant times
            DEADLINE = datetime.combine(TODAY + timedelta(days=DAYS_REMINDER_DEADLINE), DEADLINE_TIME).strftime('%A, %d. %B, %H:%M Uhr')
            ANNOUNCE_DATE = (TODAY + timedelta(days=DAYS_REMINDER_DEADLINE) + timedelta(DAYS_DEADLINE_ANNOUNCE)).strftime('%A, %d. %B')

            # Go, go, go!
            send_reminder(ANNOUNCE_DATE, DEADLINE)
            sys.exit(0)


if __name__ == '__main__':
    main()
