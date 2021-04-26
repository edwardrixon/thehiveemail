#!/usr/bin/env python

#This is a function that is used to read in whatever mailbox is passed into this function.
#Inputs are username (mailbox) and password.

import datetime
import email
import imaplib
import process_emails

#Function to connect to the mailbox and retrieve all emails
def connect_mailbox(mailbox,imap_password,mail_folder,tag):

   # Connect to imap server for each mailbox that is passed to it from email_main.py
   username = mailbox
   password = imap_password
   folder = mail_folder

   mail = imaplib.IMAP4_SSL('outlook.office365.com')
   mail.login(username, password)
   mail.list()
   mail.select(folder)

   #Collect all emails that are unread
   result, email_id = mail.uid('search', None, "UNSEEN") # (ALL/UNSEEN)

   #Display log message if failure to connect
   if 'OK' not in result:
        print((str(datetime.datetime.now())+"  FAILED to CONNECT to "+str(username)))

   num_emails = len(email_id[0].split())

   email_message=""

   if num_emails>0:
     print((str(datetime.datetime.now())+"  Emails Collected from "+str(username)+":"+str(num_emails)))
     for x in range(num_emails):
        latest_email_uid = email_id[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]

        #Need to revised this bit?#
        raw_email_string = raw_email.decode('utf-8').strip()
        email_message = email.message_from_string(raw_email_string)
        ###########################

        #Call module to process the emails that have been collected
        #Removing this to improve flow
        #process_emails.email_process(email_message,tag,mailbox,password)

   return num_emails, email_message
