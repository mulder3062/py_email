"""
split sendmail
 - if the file is a path, send the files in the path to a separate email.

usage:
    $ python split_sendmail.py --host smtp.gmail.com --port 465 --id user@gmail.com --pw idyqxxvddkekdfdf --sender foo@gmail.com --receiver bar@gmail.com -s "Hello" -e ssl -f ./sample "World"

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


def connect(host, port, user_id, pw, encrypt):
    if encrypt == 'ssl':
        server = smtplib.SMTP_SSL(host, port)
    elif encrypt == 'tls':
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()

    server.login(user_id, pw)

    return server


def send(server, sender, receiver, subject, message, file):
    try:
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


def main():
    server = None

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--host", required=True, metavar="smtp.gmail.com")
        parser.add_argument("--port", required=True, metavar=465, type=int)
        parser.add_argument("--id", metavar="userid", help="smtp login id")
        parser.add_argument("--pw", metavar="password", help="smtp login password")
        parser.add_argument("--sender", required=True, metavar="sender@domain.com")
        parser.add_argument("--receiver", required=True, metavar="receiver@domain.com")
        parser.add_argument("-f", metavar="/data/file.txt", help="attachment file")
        parser.add_argument("-s", metavar="subject")
        parser.add_argument("-e", choices=["ssl", "tls", "starttls"], help="encryption type")
        parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
        parser.add_argument("message", metavar="'message'", help="message-text")
        args = parser.parse_args()

        host = args.host
        port = args.port
        user_id = args.id
        pw = args.pw
        encrypt = args.e
        sender = args.sender
        receiver = args.receiver
        subject = args.s if args.s else "no subject"
        message = args.message
        file = args.f
        server = connect(host, port, user_id, pw, encrypt)
        cnt = 1

        if file is not None:
            if os.path.isdir(file):
                file_list = os.listdir(file)
                for f in file_list:
                    _subject = " [%03d] %s - attachment %s" % (cnt, subject, f)
                    print('SEND %s' % _subject)
                    send(server, sender, receiver, _subject, message, os.path.join(file, f))
                    cnt = cnt + 1
        else:
            send(server, sender, receiver, subject, message, file)
    except Exception as err:
        print(err)
        sys.exit(2)
    finally:
        if server is not None:
            server.quit()
            print('done')


if __name__ == '__main__':
    main()


