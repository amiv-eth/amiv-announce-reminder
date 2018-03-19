# AMIV Announce Reminder
Sends out reminder e-mails for the AMIV Announce.


## Usage
File `fridays.txt` contains the dates (in format `%d.%m.%Y`, e.g. `02.03.2018`) of the __Friday before__ the Announce is set to go out.
On those Fridays, the reminder e-mail will be sent.

The script is best triggered using a cron job. It must be called using the `--notest` flag. If it is not set, the e-mail will only be sent to `info@amiv.ethz.ch`.
Example crontab entry:

    0 8 * * FRI /path/to/amiv-announce-reminder.py --notest
