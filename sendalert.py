import time
import datetime
import smtplib
import ConfigParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

config = ConfigParser.ConfigParser()
config.read('config')

class Alertall:
  def __init__(self):
    self.EMAIL_FROM = config.get('SMTP', 'MailFrom')
    self.EMAIL_TO = config.get('SMTP', 'MailTo')
    self.SMTP_SERVER = config.get('SMTP', 'Server')
    self.SMTP_USER = config.get('SMTP', 'User')
    self.SMTP_PASS = config.get('SMTP', 'Pass')

  def sendEmail(self, attachment):
    print "Sending Email"
    SUBJECT = "Alert! Somebody Home"
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = self.EMAIL_FROM
    msg['To'] = self.EMAIL_TO

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(attachment, "rb").read())
    Encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename="'+attachment+'"')
    msg.attach(part)

    server = smtplib.SMTP()
    server.connect(self.SMTP_SERVER)
    server.login(self.SMTP_USER, self.SMTP_PASS)
    server.sendmail(self.EMAIL_FROM, self.EMAIL_TO, msg.as_string())
    print "Email Sent"
