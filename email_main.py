#!/usr/bin/env python

import read_mailbox
import json
import sys, argparse
import settings
import datetime

def readConfiguration(configfile):
    #global attachment_location, hive_address, hive_api

    #print(str(datetime.datetime.now())+"  Using Config: {0}".format(configfile))

	#Read in the configuration file called config.json
    try:
		config = json.loads(open(configfile).read())
    except IOError:
        print(str(datetime.datetime.now())+"  ERROR: Failed to read in the ",configfile," file.")
        sys.exit()

    #Read in config for the Email Servers (up to 5 mailservers defined)..yes I was lazy.
    #Read config for default file location

    attachment_location = config['ATTACHMENTS']['location']
    hive_address = config['THEHIVE']['address']
    hive_api = config['THEHIVE']['apikey']
    auto_create_tag = config['TAGS']['auto_create_tag']
    update_tag = config['TAGS']['update_tag']
    internal_email = config['INTERNAL_EMAIL']['server']
    own_domain = config['INTERNAL_EMAIL']['own_domain']
    default_recipient = config['INTERNAL_EMAIL']['default_recipient']

    settings.stored_hive_address.append(hive_address)
    settings.stored_api_key.append(hive_api)
    settings.stored_attachment_location.append(attachment_location)
    settings.stored_auto_create_tag.append(auto_create_tag)
    settings.stored_update_tag.append(update_tag)
    settings.stored_internal_email.append(internal_email)
    settings.stored_own_domain.append(own_domain)
    settings.stored_def_recipient.append(default_recipient)

    i=0

    for i in range(0,3):
       mailbox=("mailbox{0}".format(i))
       mail_server = config['MAILSERVER'][mailbox] #Name of the mailbox
       mailbox=mail_server[0]
       password=mail_server[1]
       folder=mail_server[2]
       tag=mail_server[3]

       email_ids, num_emails, emails = read_mailbox.connect_mailbox(mailbox,password,folder,tag)

       if num_emails>0:
#           I dont think it ever makes it here
#           process_emails.email_process(emails,tag,attachment_location)
            print("!!!I GOT HERE!!!")
       else:
            #print(str(datetime.datetime.now())+"  No emails to process")
            print('')

def main(argv):
    configfile = argv
    readConfiguration(configfile)

if __name__ == '__main__':
    settings.init()
    parser = argparse.ArgumentParser(description='Optional config file.')
    parser.add_argument('--config',default='config.json', help="Add a config file path")
    inputvar = parser.parse_args()
    args = inputvar.config
    main(args)
