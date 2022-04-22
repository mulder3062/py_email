"""
sendmail

usage:
    $ python sendmail.py --host smtp.gmail.com --port 465 --id user@gmail.com --pw idyqxxvddkekdfdf --sender foo@gmail.com --receiver bar@gmail.com -s "Hello" -e ssl -f /data/file.txt "World"

memo.
gmail requires setting app password.
https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637862028183203169-30180722&rd=1
"""

import smtplib
import argparse
import sys
import os
from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def get_part(filename):
    file = open(filename, "rb")
    part = MIMEApplication(file.read(), Name = os.path.basename(filename))
    part["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(filename)
    return part


def send(args):
    host = args.host
    port = args.port
    user_id = args.id
    pw = args.pw
    sender = args.sender
    receiver = args.receiver
    subject = args.s
    message = args.message
    encrypt = args.e
    file = args.f

    if encrypt == 'ssl':
        server = smtplib.SMTP_SSL(host, smtp_port)
    elif encrypt == 'tls':
        server = smtplib.SMTP(host, smtp_port)
        server.ehlo()
        server.starttls()

    try:
        server.login(user_id, pw)

        msg = MIMEMultipart()

        if subject is not None:
            msg['Subject'] = subject
        elif file is not None:
            msg['Subject'] = "attachment - %s" % file

        msg['From'] = sender
        msg['To'] = receiver
        msg['Date'] = formatdate(localtime=True)

        msg.attach(MIMEText(message))

        if file is not None:
            part = get_part(file)
            msg.attach(part)

        server.sendmail(sender, receiver, msg.as_string())
    except Exception as e:
        print(e)
    finally:
        server.close()
        server.quit()


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--host", required=True, metavar="smtp.gmail.com")
        parser.add_argument("--port", required=True, metavar=465, type=int)
        parser.add_argument("--id", metavar="userid", help="smtp login id")
        parser.add_argument("--pw", metavar="password", help="smtp login password")
        parser.add_argument("--sender", required=True, metavar="sender@domain.com")
        parser.add_argument("--receiver", required=True, metavar="receiver@domain.com")
        parser.add_argument("--split", action="store_true", help="sending files individually")
        parser.add_argument("-f", metavar="/data/file.txt", help="attachment file")
        parser.add_argument("-s", metavar="subject")
        parser.add_argument("-e", choices=["ssl", "tls", "starttls"], help="encryption type")
        parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
        parser.add_argument("message", metavar="'message'", help="message-text")
        args = parser.parse_args()
        print("send...")
        send(args)
        print('done')

    except Exception as err:
        print(err)
        sys.exit(2)


if __name__ == '__main__':
    main()


