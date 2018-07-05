#!/usr/bin/env python

#This is used to process all of thre messages that we just retrieved

import re
import create_case
import create_alert
import extraction
import datetime
import settings
import send_email
import extraction

def spam(email_message,subject,email_from,email_to,mailbox,password):
    #This will handle any message sent to spam
    template_name="SPAM INVESTIGATION"
    case_tag="spam"
    alert_pri = 1
    print(str(datetime.datetime.now())+"  Processing "+template_name+" with tag "+case_tag)
    #process_autocase(email_message,subject,template_name,case_tag,alert_pri,email_from,email_to,mailbox,password)

def brand_monitor(email_message,subject,email_from,email_to,mailbox,password):
    #This is to handle any alerts relating to brand monitoring in Domain Tools
    case_tag="Brand Alert"
    template_name="" #Dont create a case
    print(str(datetime.datetime.now())+"  Processing "+template_name+" with tag "+case_tag)
    if "Brand Monitor Alert" in subject:
        alert_title = "Domain Alert-Brand Alert"
        alert_pri = 2
    elif "Registrant Monitor Alert" in subject:
        alert_title= "Domain Alert-Registrant Alert"
        alert_pri = 1
    else:
        alert_title= "Domain Alert-General"
        alert_pri = 1

    #We arent creating a case so just send an alert
    body=""
    create_alert.prepare_alert(subject,alert_pri,body,case_tag,alert_title)

def email_pwned(email_message,subject,email_from,email_to,mailbox,password):
    #This is used for any emails picked up from the haveibeenpwned service
    case_tag="haveibeenpwned.com"
    template_name="USER INVESTIGATION"
    alert_pri = 2
    print(str(datetime.datetime.now())+"  Processing "+template_name+" with tag "+case_tag)
    #We want to automatically create a case for this
    process_autocase(email_message,subject,template_name,case_tag,alert_pri,email_from,email_to,mailbox,password)

def pastebin_alert(email_message,subject,email_from,email_to,mailbox,password):
    #This is used for any pastebin alerts.
    case_tag="Pastebin Alert"
    template_name=""
    alert_pri = 2
    print(str(datetime.datetime.now())+"  Processing "+template_name+" with tag "+case_tag)
    process_autocase(email_message,subject,template_name,case_tag,alert_pri,email_from,email_to,mailbox,password)

#Process any that will automatically generate a case in TheHive. These will always send an email.
def process_autocase(email_message,subject,template_name,case_tag,alert_pri,email_from,email_to,mailbox,password):
    #This process is kicked off when you send a message to the identified mailbox with CASE in the subject
    print(str(datetime.datetime.now())+"  Processing auto case creation for "+template_name+" with tag "+case_tag)
    subject = subject.decode('unicode_escape').encode('utf-8')
    body, url_array, mail_array = extraction.extractbody(email_message)
    file_array = extraction.extractattachments(email_message)
    TemplateName=template_name
    id, simple_id, simple_body = create_case.prepare_case_template(subject,alert_pri,body,"AutoCreated",case_tag,TemplateName)
    create_case.prepare_mail_observable(id, mail_array)
    create_case.prepare_url_observable(id, url_array)
    create_case.prepare_file_observable(id, file_array)
    send_email.send_mailbox(body,simple_id,email_from, email_to, subject,mailbox,password)

#This will add a task to an existing case
def update_autocase(email_message,subject):
#    update_tag=''.join(settings.stored_update_tag[0])
#    update_tag = "r'"+str(update_tag)+"(\w+)'"

    print(str(datetime.datetime.now())+"  Starting update of existing case.")
    
    #Create a search to find the hive case number
    revised = re.search(r'HIVE-CASE#(\w+)', subject)  

    id = revised.group(1) #Extract the real case number

    print(str(datetime.datetime.now())+"  Case number:"+id+" Extracted.")
    body, url_array, mail_array = extraction.extractbody(email_message)
    print(str(datetime.datetime.now())+"  Extracting attachments")
    file_array = extraction.extractattachments(email_message)
    create_case.prepare_mail_observable(id, mail_array)
    create_case.prepare_url_observable(id, url_array)
    create_case.prepare_file_observable(id, file_array)
    #We need to add something to the task called History that we have setup
    full_task_id = create_case.search_case(id,body,file_array)
    create_case.add_task_log(full_task_id,body,file_array)

