# AMIV Announce Reminder
Sends out reminder e-mails for the AMIV Announce.


## Usage
File `reminder_days.txt` contains the dates (in format `%d.%m.%Y`, e.g. `02.03.2018`) of the __days when the reminder is sent__.

The script is best triggered using a cron job. It must be called using the `--notest` flag. If it is not set, the e-mail will only be sent to `info@amiv.ethz.ch`.
Example crontab entry (runs every day at 8am):

    0 8 * * * /path/to/amiv-announce-reminder.py --notest
