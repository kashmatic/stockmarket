import smtplib

from email.mime.text import MIMEText

msg = MIMEText("Hello")

msg['Subject'] = 'Test'
msg['From'] = ''
