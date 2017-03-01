#! /usr/bin/python3
# authorization code: kzknlhezuhwijiec
# send an email using python

import smtplib
from email.mime.text import MIMEText

# parameters
subject = "Python Email Demo"
message = " Hello: \n\nCongratulations, you are successful!"
smtp_server = "smtp.qq.com"
from_addr = "***@qq.com"
password = "Your password"
to_addr = "Your destination"

def sendMail(subject,body):
    global smtp_server
    global from_addr
    global password
    global to_addr

    msg=MIMEText(body,'plain','utf-8')
    msg['Subject']=subject
    msg['From']=from_addr
    msg['To']=to_addr

    server=smtplib.SMTP(smtp_server,587)
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr,password)
    server.sendmail(from_addr,to_addr,msg.as_string())
    server.quit()

if __name__ == '__main__':
    sendMail(subject,message)


