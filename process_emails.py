#!/usr/bin/env python

#This is used to process all of thre messages that we just retrieved

from email.header import decode_header, make_header
import modules
import email
import datetime
import send_email
import settings

#This module will process the email sent to it and select relevant modules to execute.
def email_process(emails,tag,mailbox,password):
    update_tag=''.join(settings.stored_update_tag[0])
    auto_create_tag=''.join(settings.stored_auto_create_tag[0])
    email_message = emails

     #Extract the Date -Not used yet
     #date_tuple = email.utils.parsedate_tz(emails['Date'])
     #date_tuple = raw_email.date

     #if date_tuple:
     #   local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
     #   local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))

     #Common Extractions for all discovered emails to be searched on
    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
    email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
    subject = decode_header(email_message.get('subject'))[0][0]

    print("This is the tag:"+tag)
    #If the email has the autocase trigger in it then regardless of which mailbox it came from.
    if str(update_tag) in str(subject):
        modules.update_autocase(email_message,subject) #run module to update an existing case.
    elif str(auto_create_tag) in str(subject):
        template_name="AUTOCASE"
        case_tag="Auto created general case"
        alert_pri = 1
        modules.process_autocase(email_message,subject,template_name,case_tag,alert_pri,email_from,email_to,mailbox,password)
        
    #Process messages tagged as spam. These will always create a case, extract attachments etc.
    elif tag=="spam":
        modules.spam(email_message,subject,email_from,email_to,mailbox,password)

    #Process messages tagged as security. This will call modules that determines what happens next based on search criteria
    elif tag=="security":
        #Process messages from the security mailbox. Case extractions depends on what the subject is etc
        if "noreply@haveibeenpwned.com" in email_from and "multi-domain" not in subject:
            modules.email_pwned(email_message,subject,email_from,email_to,mailbox,password) #
        elif "domaintools.com" in email_from:
            modules.brand_monitor(email_message,subject,email_from,email_to,mailbox,password)
        else:
            #If it gets to here unset the read flag (so we know whats been read but not processed) - NOT IMPLEMENTED YET
            result, email_data = mail.uid('store',latest_email_uid,'-FLAGS','\\Seen')
            print("")
    else:
        print(str(datetime.datetime.now())+"  No TAGs have been applied to the email")


