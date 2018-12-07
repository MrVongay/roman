import asyncore
import os
import smtpd
import datetime

from mailer import Mailer
from mailer import Message


class CustomSMTPServer(smtpd.SMTPServer):

    def __init__(self, localaddr, remoteaddr, path):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        self.path = path


    def process_message(self, peer, mailfrom, rcpttos, data):
        filename = os.path.join(self.path, "smtp_relay.%s.%s.txt" % (mailfrom, datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")))
        filename = filename.replace("<", "").replace(">", "")
        f = file(filename, "w")
        f.write(data + "\n")
        f.close()
        message("Mail to %s saved" % filename)

        mail_from = "osboxes@mvongay.au"
        mail_list = "mvongay@mvongay.au"
        message = Message(From=mail_from,
        To=mail_list,
        Subject="Test")
        message.Body = (data)
        sender = Mailer("127.0.0.1:25")
        sender.send(message)


log_file = None


def message(text):
    global log_file
    if log_file is not None:
        f = file(log_file, "a")
        f.write(text + "\n")
        f.close()
    else:
        print text


if __name__ == "__main__":

        server = CustomSMTPServer(('127.0.0.1', 8025), ('127.0.0.1', 25), '/home/mvongay/GIT/DLAR')
        asyncore.loop()
