#!/usr/bin/env python

import mailbox
import requests
import sys
import json
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact
import settings

def prepare_alert(subject,indicatorlevel,emailbody,alerttype,tag):

    hive_address=''.join(settings.stored_hive_address[0])
    hive_api=''.join(settings.stored_api_key[0])

    #Define the connection to thehive installation (including the generated API key).
    api = TheHiveApi(hive_address,hive_api,None, {'http': '', 'https': ''})
 
    # Prepare the sample Alert
	
    print("Preparing the alert for", alerttype)
    sourceRef = str(uuid.uuid4())[0:6]
    alert = Alert(title=subject,
        	tlp=indicatorlevel,
        	tags=[tag],
        	description=emailbody,
       		type=alerttype,
        	source='instance1',
        	sourceRef=sourceRef,
		artifacts="")
	
	# Create the Alert
    print('Create Alert')
    print('-----------------------------')
    id = None
    response = api.create_alert(alert)
    if response.status_code == 201:
                print("Alert created sucessfully!")
#    		print(json.dumps(response.json(), indent=4, sort_keys=True))
#    		print('')
    		id = response.json()['id']
    else:
                print("Unable to create alert")
#   		print('ko: {}/{}'.format(response.status_code, response.text))
    		sys.exit(0)

	# Get all the details of the created alert
    print('Get created alert {}'.format(id))
    print('-----------------------------')
    response = api.get_alert(id)
    if response.status_code == requests.codes.ok:
#    		print(json.dumps(response.json(), indent=4, sort_keys=True))
    		print('')
    else:
                print("Error retreiving the alert!")
		print('ko: {}/{}'.format(response.status_code, response.text))


def skip_email():
        print("Skip it!")
        return
