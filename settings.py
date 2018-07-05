#!/usr/bin/env python

#This is used purely to store the contents of the configuration file in memory so that all modules can access these variables
def init():
    global stored_hive_address, stored_api_key, stored_attachment_location, stored_auto_create_tag, \
    stored_update_tag, stored_internal_email, stored_own_domain, stored_def_recipient, stored_security_recipients, \
    stored_email_tag_line, stored_remove_email_observables, stored_remove_file_observables,stored_remove_url_observables,\
    stored_remove_file_attachments
    
    stored_hive_address=[]
    stored_api_key=[]
    stored_attachment_location=[]
    stored_auto_create_tag=[]
    stored_update_tag=[]
    stored_internal_email=[]
    stored_own_domain=[]
    stored_def_recipient=[]
    stored_security_recipients=[]
    stored_email_tag_line=[]
    stored_remove_email_observables=[]
    stored_remove_file_observables=[]
    stored_remove_url_observables=[]
    stored_remove_file_attachments=[]