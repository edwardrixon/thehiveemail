#!/usr/bin/env python

#This is used to process all of thre messages that we just retrieved

from __future__ import print_function
from __future__ import unicode_literals
from optparse import OptionParser

import re
import create_case
import create_alert
import extraction
import os
import mimetypes
import requests
import sys
import json
import uuid
import time
import imaplib
import email
import datetime
import mailbox
import html2text
import settings
import send_email

#import mailparser

def brand_monitor(email_message,subject):
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

def email_pwned(email_message,subject,email_from,email_to,password):
    #This is used for any emails picked up from the haveibeenpwned service
    case_tag="haveibeenpwned.com"
    template_name="USER INVESTIGATION"
    alert_pri = 2
    print(str(datetime.datetime.now())+"  Processing "+template_name+" with tag "+case_tag)

    #We want to automatically create a case for this
    case_id,simple_id,body = process_autocase(email_message,subject,template_name,case_tag)
    send_email.send_mailbox(body,simple_id,email_from, email_to, subject,mailbox,password) 

def pastebin_alert(email_message,subject):
    #This is used for any pastebin alerts.
    case_tag="Pastebin Alert"
    template_name=""
    alert_pri = 2
    print(str(datetime.datetime.now())+"  Processing "+template_name+" with tag "+case_tag)

def process_autocase(email_message,subject,template_name,case_tag):
    #This process is kicked off when you send a message to the identified mailbox with CASE in the subject

    #raw_email = mailparser.parse_from_string(email_message)   
    attachment_location=''.join(settings.stored_attachment_location[0])
    
    #email_message = raw_email

    subject = subject.decode('unicode_escape').encode('utf-8')
#    print("DECODED SUBJECT:",subject)

    body, url_array, mail_array = extraction.extractbody(email_message)
    file_array = extraction.extractattachments(email_message,attachment_location)
    TemplateName=template_name
    id, simple_id, simple_body = create_case.prepare_case_template(subject,1,body,"AutoCreated",case_tag,TemplateName)
    create_case.prepare_mail_observable(id, mail_array)
    create_case.prepare_url_observable(id, url_array)
    create_case.prepare_file_observable(id, file_array)
    #file_array = extraction.extractattachments(email_message,attachment_location)
    return simple_id, simple_body

def update_autocase(email_message,subject):
    update_tag=''.join(settings.stored_update_tag[0])
    #Extract the case number
    print(str(datetime.datetime.now())+"  Starting update of existing case.")
    attachment_location=''.join(settings.stored_attachment_location[0])
    revised = re.search(r'HIVE-CASE#(\w+)', subject)    
    id = revised.group(1)

    print(str(datetime.datetime.now())+"  Case number:"+id+" Extracted.")
    body, url_array, mail_array = extraction.extractbody(email_message)
    print(str(datetime.datetime.now())+"  Extracting attachments")
    file_array = extraction.extractattachments(email_message,attachment_location)

    #We need to add something to the task called History that we have setup
    TemplateName="AUTOCASE"
    create_case.search_case(id,body,file_array)

