#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from lorem import get_paragraph
import time


# Connect to Outlook's SMTP server
smtp_server = 'smtp.office365.com'
smtp_port = 587  # TLS port
smtp_username = "thedorothea@outlook.com"
smtp_password = 'dorothea_pass'
recipient_email = smtp_username

subject = 'DOROTHEA autogenerated mail'

for i in range(10):

    body = get_paragraph(count=2)

    # Create the MIMEText object
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    time.sleep(60)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, recipient_email, msg.as_string())
        print('Email sent successfully')
    except Exception as e:
        print('Error:', str(e))
    finally:
        server.quit()
