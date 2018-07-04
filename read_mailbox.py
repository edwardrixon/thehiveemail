#!/usr/bin/env python

#This is a function that is used to read in whatever mailbox is passed into this function.
#Inputs are username (mailbox) and password.

import datetime
import email
import imaplib
import process_emails
#from flanker import addresslib
#from flanker import mime

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
 
   if result == 'OK':
        print(str(datetime.datetime.now())+"  CONNECTED to "+str(username))
   else:
        print(str(datetime.datetime.now())+"  FAILED to CONNECT to "+str(username))

   num_emails = len(email_id[0].split())

   print(str(datetime.datetime.now())+"  Emails Collected from "+str(username)+":"+str(num_emails))

   # Convert the messages into email message object.

   email_array = []

   if num_emails>0:
     for x in range(num_emails):
        latest_email_uid = email_id[0].split()[x]
        #Open the email but as string format
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8').strip()
        email_message = email.message_from_string(raw_email_string)
        #TESTER
        #msg = mime.from_string(raw_email)
        #print("HEADERS:",msg.headers.items())

        #if msg.content_type.is_singlepart():
        #  msg.body
        # parts if message is multipart
        #if msg.content_type.is_multipart():
        #  msg.parts
        # enclosed message
        #if msg.content_type.is_message_container():
        #  msg.enclosed

        #for part in mail.parts:
        #  print 'Content-Type: {} Body: {}'.format(part, part.body)
        #  for part in
        #print("BODY:",mail.body)
        #print(mail.enclosed)

        #Decode the string and strip out bad characters.
        #raw_email_string = raw_email.decode('utf-8').strip()
        #email_message = email.message_from_string(raw_email_string)

        #Process the email that has been recieved
        #process_emails.email_process(email_message,tag,mailbox,password)
        process_emails.email_process(email_message,tag,mailbox,password)

   else:
      email_message=""

   return email_id, num_emails, email_array
