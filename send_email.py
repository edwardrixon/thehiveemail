#!/usr/bin/env python

#This is a function that is used to read in whatever mailbox is passed into this function.
#Inputs are username (mailbox) and password.

import datetime
import email
import imaplib
import json
import mailbox
import smtplib
import sys
import time
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import email_main
import process_emails
import settings


#Function to connect to the mailbox and retrieve all emails
def send_mailbox(email_message,case_id,email_from,email_to,full_subject,mailbox,password):

   mailbox=''.join(settings.stored_internal_email[0])
   own_domain=''.join(settings.stored_own_domain[0])
   default_recipient=''.join(settings.stored_def_recipient[0])

   #Strip [CASE] from the subject so it looks nicer.
   subject = full_subject.replace('[CASE]','')

   # Connect to imap server
   #username = mailbox
   password = password
   #folder = mail_folder
   subject = "[HIVE-CASE#"+str(case_id)+"]:"+subject

   msg = MIMEMultipart()
   msg['From'] = email_to
   msg['To'] = email_from
   msg['Subject'] = subject

   if str(own_domain) not in email_from:
       print(str(datetime.datetime.now())+"  External recipient detected ("+email_from+"). This has not been sent from "+str(own_domain)+". Mail to be sent to default mailbox.")
       email_from=default_recipient
     
   print(str(datetime.datetime.now())+"  Sending email to "+email_from+" from "+email_to+" with subject "+subject)
   
   #Need some logic here to deal with messages that wont send due to the UnicdeEncodeError when doing MIMEText below.
   try:
       #Send the message as is as there is nothing wrong with it
       msg.attach(MIMEText(email_message,'plain'))
       text=msg.as_string()
   except UnicodeEncodeError:
       #Its broken, temporary fix as had enough of the "Encode/Decode Dance of Doom"
       print(str(datetime.datetime.now())+"  Encoding gone amok, trying another type.")
       text=msg.as_string()
       
   mail = smtplib.SMTP(mailbox)

   #Send all emails to default mailbox for now
   email_to = default_recipient
#   mail.ehlo()
#   mail.set_debuglevel(1)
#   mail.login(username, password)
#######################################################
   mail.sendmail(email_to,email_from,text)
#######################################################
   print(str(datetime.datetime.now())+"  Disconnecting from internal mail server.")
   mail.quit()
   