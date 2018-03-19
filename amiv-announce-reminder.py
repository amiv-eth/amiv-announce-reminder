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
                    DEADLINE_TIME)


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

    # Read 'reminder fridays'
    with open('fridays.txt') as friday_file:
        FRIDAYS = friday_file.readlines()
    
    # Strip whitespace
    FRIDAYS = [friday.strip() for friday in FRIDAYS]

    # Check if today is a reminder Friday
    TODAY = date.today()
    for friday in FRIDAYS:
        # Skip blank lines
        if not friday:
            continue

        if TODAY == datetime.strptime(friday, '%d.%m.%Y').date():
            # Deadline is Tuesday, 4 days after Friday
            DEADLINE = datetime.combine(TODAY + timedelta(days=4), DEADLINE_TIME).strftime('%A, %d. %B, %H:%M Uhr')

            # Announce is send Wednesday, 5 days after Friday
            ANNOUNCE_DATE = (TODAY + timedelta(days=5)).strftime('%A, %d. %B')

            # Go, go, go!
            send_reminder(ANNOUNCE_DATE, DEADLINE)
            sys.exit(0)


if __name__ == '__main__':
    main()
