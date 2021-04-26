#!/usr/bin/env python

import read_mailbox
import json
import sys, argparse
import settings
import datetime
import process_emails

def readConfiguration(configfile):
	#Read in the configuration file that is called by email_main. e.g. python email_main.py --config=config.json
    try:
		config = json.loads(open(configfile).read())
    except IOError:
        print((str(datetime.datetime.now())+"  ERROR: Failed to read in the ",configfile," file."))
        sys.exit()

    #Read in the configuration file.
    attachment_location = config['ATTACHMENTS']['location'] #Default location for attachments
    hive_address = config['THEHIVE']['address'] #Address of TheHive server
    hive_api = config['THEHIVE']['apikey'] #API Key used to access TheHive server
    auto_create_tag = config['TAGS']['auto_create_tag'] #Tag that is detected in emails to automatically create a case
    update_tag = config['TAGS']['update_tag'] #Tag that is detected in emails to automatically update existing cases
    internal_email = config['INTERNAL_EMAIL']['server'] #The name of the internal email server to send emails
    own_domain = config['INTERNAL_EMAIL']['own_domain'] #The email domain used by the company hosting TheHive
    default_recipient = config['INTERNAL_EMAIL']['default_recipient'] #A default email recipient that will recieve emails
    security_recipients = config['INTERNAL_EMAIL']['security_team'] #The list of recipients in the Security team to recieve emails
    email_tag_line = config['INTERNAL_EMAIL']['email_tag_line'] #Standard message that will be included in each email.
    remove_email_observables = config['OBSERVABLES']['remove_email_observables'] #List of observables to be ignored i.e. your internal email addressess and domains
    remove_file_observables = config['OBSERVABLES']['remove_file_observables'] #List of observables to be ignored i.e. your internal email addressess and domains
    remove_url_observables = config['OBSERVABLES']['remove_url_observables'] #List of observables to be ignored i.e. your internal email addressess and domains
    remove_file_attachments = config['OBSERVABLES']['remove_file_attachments'] #List of observables to be ignored i.e. your internal email addressess and domains


    #Store all of these variables in settings.py so that they can be used for all modules and python programs.
    settings.stored_hive_address.append(hive_address)
    settings.stored_api_key.append(hive_api)
    settings.stored_attachment_location.append(attachment_location)
    settings.stored_auto_create_tag.append(auto_create_tag)
    settings.stored_update_tag.append(update_tag)
    settings.stored_internal_email.append(internal_email)
    settings.stored_own_domain.append(own_domain)
    settings.stored_def_recipient.append(default_recipient)
    settings.stored_security_recipients.append(security_recipients)
    settings.stored_email_tag_line.append(email_tag_line)
    settings.stored_remove_email_observables.append(remove_email_observables)
    settings.stored_remove_file_observables.append(remove_file_observables)
    settings.stored_remove_url_observables.append(remove_url_observables)
    settings.stored_remove_file_attachments.append(remove_file_attachments)

    i=0
   
    #I was lazy and put list of mailboxes to read in configuration file. Read them in here.
    for i in range(0,3):
        mailbox=("mailbox{0}".format(i))
        mail_server = config['MAILSERVER'][mailbox] #Read in the name of the mailbox
        mailbox=mail_server[0] 
        password=mail_server[1]
        folder=mail_server[2]
        tag=mail_server[3]

        #Execute function to read the mailbox and return the email ids, number collected and actual emails
        num_emails, emails = read_mailbox.connect_mailbox(mailbox,password,folder,tag)

        if num_emails>0:
            #Moved logic to here to process emails.
            print((str(datetime.datetime.now())+"  Processing "+str(num_emails)+" emails."))
            process_emails.email_process(emails,tag,mailbox,password)

def main(argv):
    configfile = argv
    readConfiguration(configfile) 

if __name__ == '__main__':
    settings.init() #Read in 'global' variable names
    parser = argparse.ArgumentParser(description='Optional config file.')
    parser.add_argument('--config',default='config.json', help="Add a config file path")
    inputvar = parser.parse_args()
    args = inputvar.config
    main(args)
