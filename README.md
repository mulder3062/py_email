# py_email
Send mail using smtplib of python 3.

* sendmail.py: you can send 1 attachment.
* split_sendmail.py: send the file in the path to individual mail.

# sendmail.py
```
usage: sendmail.py [-h] --host smtp.gmail.com --port 465 [--id userid] [--pw password] --sender sender@domain.com --receiver receiver@domain.com [--split] [-f /data/file.txt] [-s subject] [-e {ssl,tls,starttls}] [-v] 'message'

positional arguments:
'message'             message-text

options:
-h, --help            show this help message and exit
--host smtp.gmail.com
--port 465
--id userid           smtp login id
--pw password         smtp login password
--sender sender@domain.com
--receiver receiver@domain.com
--split               sending files individually
-f /data/file.txt     attachment file
-s subject
-e {ssl,tls,starttls}
encryption type
-v, --verbose         increase output verbosity
```

example:

```
$ python sendmail.py --host smtp.gmail.com --port 465 --id user@gmail.com --pw idxxxxxxxxxxxxxx --sender foo@gmail.com --receiver bar@gmail.com -s "Hello" -e ssl -f /data/file.txt "World"
```



# split_sendmail.py
```
usage: split_sendmail.py [-h] --host smtp.gmail.com --port 465 [--id userid] [--pw password] --sender sender@domain.com --receiver receiver@domain.com [-f /data/file.txt] [-s subject] [-e {ssl,tls,starttls}] [-v] 'message'

positional arguments:
'message'             message-text

options:
-h, --help            show this help message and exit
--host smtp.gmail.com
--port 465
--id userid           smtp login id
--pw password         smtp login password
--sender sender@domain.com
--receiver receiver@domain.com
-f /data/file.txt     attachment file
-s subject
-e {ssl,tls,starttls}
encryption type
-v, --verbose         increase output verbosity
```

example
```
$ python split_sendmail.py --host smtp.gmail.com --port 465 --id user@gmail.com --pw idxxxxxxxxxxxxxx --sender foo@gmail.com --receiver bar@gmail.com -s "Hello" -e ssl -f ./sample "World"
```