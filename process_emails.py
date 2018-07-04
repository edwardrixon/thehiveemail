#!/usr/bin/env python

#This is used to process all of thre messages that we just retrieved

#from __future__ import print_function
#from __future__ import unicode_literals
#from optparse import OptionParser
from email.header import decode_header, make_header
import modules
import email
import datetime
import send_email
import settings
#import mailparser

def email_process(emails,tag,mailbox,password):
     #raw_email = mailparser.parse_from_string(emails)
     update_tag=''.join(settings.stored_update_tag[0])
     auto_create_tag=''.join(settings.stored_auto_create_tag[0])
     email_message = emails

     #Extract the Date
     date_tuple = email.utils.parsedate_tz(emails['Date'])
     #date_tuple = raw_email.date

     if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))

     #Common Extractions for all discovered emails to be searched on
     email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
     email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
     #email_to = raw_email.to
     #print(email_to)
     subject, encoding = decode_header(email_message.get('subject'))[0]
     #subject = raw_email.subject
     #print(subject)
     #print("Encoding for subject is :", encoding)
     
     if tag=="spam":
        #Process messages from the spam mailbox. These will always create a case, extract attachments etc.
        template_name="SPAM INVESTIGATION"
        case_tag="spam"
        print(str(datetime.datetime.now())+"  Processing "+template_name+" with tag "+case_tag)
        case_id,simple_id,body = modules.process_autocase(email_message,subject,template_name,case_tag)
        send_email.send_mailbox(body,simple_id,email_from, email_to, subject,mailbox,password)
     elif tag=="security":
        #Process messages from the security mailbox
        if auto_create_tag in subject:
         #This is just a test, eventually all emails will need an autoresponse
            template_name="AUTOCASE"
            case_tag=""
            print(str(datetime.datetime.now())+"  Processing "+template_name+" with tag "+case_tag)
            case_id,simple_id,body = modules.process_autocase(email_message,subject,template_name,case_tag)
            send_email.send_mailbox(body,simple_id,email_from, email_to, subject,mailbox,password)
        elif update_tag in subject:
           modules.update_autocase(email_message,subject)   
        elif "noreply@haveibeenpwned.com" in email_from and "multi-domain" not in subject:
            case_tag="haveibeenpwned.com"
            template_name="USER INVESTIGATION"
            print(str(datetime.datetime.now())+"  Processing "+template_name+" with tag "+case_tag)
            case_id,simple_id,body = modules.process_autocase(email_message,subject,template_name,case_tag)
            send_email.send_mailbox(body,simple_id,email_from, email_to, subject,mailbox,password) 

     elif tag=="securityalerts":
        #Process messages from the security alerts mailbox
        print("SECURITYALERTS")

     else:
        print(str(datetime.datetime.now())+"  No TAGs have been applied to the email")


