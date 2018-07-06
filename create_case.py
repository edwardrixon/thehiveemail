#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals

import email_main
import re
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
from thehive4py.api import TheHiveApi
from thehive4py.query import *
from thehive4py.models import Alert, AlertArtifact, Case, CaseObservable, CaseTask, CaseTaskLog, CustomFieldHelper, CaseTemplate
import settings

def find_case_id(title, query, range, sort):
    hive_address=''.join(settings.stored_hive_address[0])
    hive_api=''.join(settings.stored_api_key[0])
    #Define the connection to thehive installation (including the generated API key).
    api = TheHiveApi(hive_address,hive_api,None, {'http': '', 'https': ''})

    response = api.find_cases(query=query, range=range, sort=sort)

    if response.status_code == 200:
        test = json.dumps(response.json(), indent=4, sort_keys=True)
        resp = json.loads(test)
        try:
                full_case_id = resp[0]['id']
                print(str(datetime.datetime.now())+"  Case: "+str(query)+" found. Extracted full case id number ("+str(full_case_id)+").")
                return full_case_id
        except IndexError:
                print(str(datetime.datetime.now())+"  Case: "+str(query)+ "has not been found.")
    else:
#        print('ko: {}/{}'.format(response.status_code, response.text))
        sys.exit(0)

def find_task_log_id(query):
    hive_address=''.join(settings.stored_hive_address[0])
    hive_api=''.join(settings.stored_api_key[0])
    #Define the connection to thehive installation (including the generated API key).
    api = TheHiveApi(hive_address,hive_api,None, {'http': '', 'https': ''})

    response = api.get_case_tasks(case_id=query, range="all", sort=[])

    if response.status_code == 200:
        test = json.dumps(response.json(), indent=4, sort_keys=True)
        resp = json.loads(test)
        
        #I now need to search for a task called History
        for item in resp:
                if item['title'] == 'History':
                        full_task_id = item['id']
			print("I found the task, it id:",full_task_id)
                        return full_task_id
      
        print(str(datetime.datetime.now())+"  I didn't find a History task!")
    else:
        print('ko: {}/{}'.format(response.status_code, response.text))
        print("NOT HERE")
        sys.exit(0)       

def add_task_log(full_task_id,body,file_array):
        hive_address=''.join(settings.stored_hive_address[0])
        hive_api=''.join(settings.stored_api_key[0])
    
        #Define the connection to thehive installation (including the generated API key).
        api = TheHiveApi(hive_address,hive_api,None, {'http': '', 'https': ''})

        #Strip the message of any old replies---difficult as I have already made it a plain text file so all encoded stuff gone!.
        #string_list = re.findall(r"\w+\s+\w+[,]\s+\w+\s+\d+[,]\s+\d+\s+\w+\s+\d+[:]\d+\s+\w+.*", body) # regex for On Thu, Mar 24, 2011 at 3:51 PM
        #res = body.split(string_list[0]) # split on that match
        #print(res[0]) # get before string of the regex

        #print("So is this the split message?:",res[0])

        #Later add on file=file_array
        tasklog = CaseTaskLog(message=body, file="")

        #Need to also add some observables to this
        response = api.create_task_log(full_task_id,tasklog)

        if response.status_code == 201:
    		#print(json.dumps(response.json(), indent=4, sort_keys=True))
                print('str(datetime.datetime.now())+"  Observable succesfully created.")
    	else:
                print('ko: {}/{}'.format(response.status_code, response.text))
    		sys.exit(0)

def search_case(case_id):
        full_case_id = find_case_id("CaseSearchQuery", Eq('caseId', case_id), 'all', [])
        full_task_id = find_task_log_id(full_case_id)

        return full_task_id, full_case_id


def prepare_case_template(subject,indicatorlevel,emailbody,casetype,tag,templatename):
        hive_address=''.join(settings.stored_hive_address[0])
        hive_api=''.join(settings.stored_api_key[0])

        #Define the connection to thehive installation (including the generated API key).
        api = TheHiveApi(hive_address,hive_api,None, {'http': '', 'https': ''})

        # Prepare the sample Case based on a Template
        print(str(datetime.datetime.now())+"  Preparing the case for "+casetype)

        case = Case(title=subject,
        	tlp=indicatorlevel,
        	tags=[tag],
        	description=emailbody,
                template=templatename,
#       		type=alerttype,
#        	source='instance1',
#        	sourceRef=sourceRef,
#		artifacts="")
                )
	
	# Create the Case

        id = None
#################################################
	response = api.create_case(case)
#################################################

	if response.status_code == 201:
#    		print(json.dumps(response.json(), indent=4, sort_keys=True))
    		print('')
    		id = response.json()['id']
                simple_id = response.json()['caseId']
	else:
   		print('ko: {}/{}'.format(response.status_code, response.text))
    		sys.exit(0)

	# Get all the details of the created case
	print(str(datetime.datetime.now())+"  Getting created case {}".format(id))
	response = api.get_case(id)
	if response.status_code == requests.codes.ok:
#    		print(json.dumps(response.json(), indent=4, sort_keys=True))
                print('str(datetime.datetime.now())+"  Observable succesfully created.")
                
	else:
		print('ko: {}/{}'.format(response.status_code, response.text))

        return id, simple_id, emailbody

def prepare_mail_observable(id,mail_array):
#We will need to run through the arrays to extract the values.
   #Define the connection to thehive installation (including the generated API key).
   hive_address=''.join(settings.stored_hive_address[0])
   hive_api=''.join(settings.stored_api_key[0])

   api = TheHiveApi(hive_address, hive_api,None, {'http': '', 'https': ''})

   for mailaddress in mail_array:
      print(str(datetime.datetime.now())+"  Creating mail observable:"+str(mailaddress))
      domain = CaseObservable(dataType='mail',
                        data=[mailaddress],
                        tlp=0,
                        ioc=False,
                        tags=['ExtractedEmails'],
                        message='Emails Extracted'
                        )
      response = api.create_case_observable(id, domain)

      if response.status_code == 201:
#         print(json.dumps(response.json(), indent=4, sort_keys=True))
         print('str(datetime.datetime.now())+"  Observable succesfully created.")
      elif response.status_code == 400:
	 print('str(datetime.datetime.now())+"  Email Observable already exists")
      else:
         print(str(datetime.datetime.now())+"  Error creating Email Observables.")
         print('ko: {}/{}'.format(response.status_code, response.text))
         sys.exit(0)   

def prepare_url_observable(id,url_array):
   hive_address=''.join(settings.stored_hive_address[0])
   hive_api=''.join(settings.stored_api_key[0])

#We will need to run through the arrays to extract the values.
       #Define the connection to thehive installation (including the generated API key).
   api = TheHiveApi(hive_address, hive_api,None, {'http': '', 'https': ''})

   for urladdress in url_array:
      print(str(datetime.datetime.now())+"  Creating url observable:"+urladdress)
      domain = CaseObservable(dataType='url',
                        data=[urladdress],
                        tlp=0,
                        ioc=False,
                        tags=['ExtractedUrls'],
                        message='Urls Extracted'
                        )
      response = api.create_case_observable(id, domain)

      if response.status_code == 201:
#         print(json.dumps(response.json(), indent=4, sort_keys=True))
         print('str(datetime.datetime.now())+"  Observable succesfully created.")
      elif response.status_code == 400:
	 print('str(datetime.datetime.now())+"  URL Observable already exists") 
      else:
         print(str(datetime.datetime.now())+"  Error creating URL Observables.")
         print('ko: {}/{}'.format(response.status_code, response.text))
         sys.exit(0)


def prepare_subject_observable(id,subject):
   hive_address=''.join(settings.stored_hive_address[0])
   hive_api=''.join(settings.stored_api_key[0])

       #Define the connection to thehive installation (including the generated API key).
   api = TheHiveApi(hive_address, hive_api,None, {'http': '', 'https': ''})

   print(subject)

   print('Create subject observable')
   print('---------------------')
   domain = CaseObservable(dataType='subject',
                        data=[subject],
                        tlp=0,
                        ioc=False,
                        tags=['ExtractedSubject'],
                        message='Subject Extracted'
                        )
   response = api.create_case_observable(id, domain)

   if response.status_code == 201:
#      print(json.dumps(response.json(), indent=4, sort_keys=True))
      print('str(datetime.datetime.now())+"  Observable succesfully created.")
   elif response.status.code == 400:
      print('str(datetime.datetime.now())+"  Subject Observable already exists")
   else:
      print(str(datetime.datetime.now())+"  Error creating Subject Observables.")
      print('ko: {}/{}'.format(response.status_code, response.text))
      sys.exit(0)


def prepare_file_observable(id,file_array):
#We will need to run through the arrays to extract the values.
#Define the connection to thehive installation (including the generated API key).
   hive_address=''.join(settings.stored_hive_address[0])
   hive_api=''.join(settings.stored_api_key[0])

   api = TheHiveApi(hive_address, hive_api,None, {'http': '', 'https': ''})

   for fileaddress in file_array:
      print(str(datetime.datetime.now())+"  Creating file observable:"+fileaddress)

      print('Create file observable')
      print('---------------------')
      domain = CaseObservable(dataType='file',
                        data=[fileaddress],
                        tlp=0,
                        ioc=False,
                        tags=['AttachedFiles'],
                        message='Files Attached'
                        )
      response = api.create_case_observable(id, domain)

      if response.status_code == 201:
#         print(json.dumps(response.json(), indent=4, sort_keys=True))
         print('str(datetime.datetime.now())+"  Observable succesfully created.")      
      elif response.status_code == 400:
         print('str(datetime.datetime.now())+"  Attachment already exists")
      else:
         print(str(datetime.datetime.now())+"  Error creating URL Observables.")
         print('ko: {}/{}'.format(response.status_code, response.text))
         sys.exit(0)
