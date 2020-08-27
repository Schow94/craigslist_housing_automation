## import required modules
## modules can be imported using pip﻿
import smtplib
from email.mime.text import MIMEText as text
import os

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

## declare a function that sends email
## this currently works only with gmail but can work with other
## email providers as well with slight modification
## remember to turn on "Access for less secure apps" in GMail via Link beforehand
## https://www.google.com/settings/security/lesssecureapps


def test_sendmail(email, subject):
    """ This script contains the parameters required for sending the email """
    to_address = email  ## change this
    body = subject
    subject = subject
    sendmail(to_address, subject, body)


def sendmail(to_address, subject, body):
    from_address = 'YOUR EMAIL GOES HERE'  ## change this
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'YOUR EMAIL GOES HERE'  ## change this
    smtp_password = 'YOUR PASSWORD GOES HERE'  ## change this

    msg = text(body)
    # msg = {}
    # msg['Subject'] = subject
    # msg['From'] = from_address
    # msg['To'] = to_address

    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()
