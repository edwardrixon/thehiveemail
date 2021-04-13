# thehiveemail
System that is used primarily to read from a defined set of mailboxes and based upon content that is defined by the administrator these are extracted and then cases are automatically created in the hive (if required).

Primarily does the following:
Ad-Hoc Case Creation via emails.
Autocase Creation based on mailbox criteria.
Auto-update of case task log with associated emails.

This is also coupled with scripting that regularly sends slack messages based on updates etc (havent added this in the git repo yet).

Ad-hoc Case Creation:
1. If you wish an email to be automatically created as a case in TheHive then the subject of the email is modified to include a configurable tag i.e. [HIVE]
2. Email is sent to whichever pre-defined mailbox.
3. thehivemail will pickup the email and create a case in TheHive as well as extract any attachments and other observables.
4. A response email will be sent back to the sender (only if they are inside the organisation) with the subject altered to include another configurable tag as well as the case number i.e. [HIVE NO:123].

AutoCase Creation:
1. Sepcific mailboxes, subjects or other search criteria can be identified and will automatically create a case.
2. The case information will be sent to the members of the security team as well as the original sender. 

AutoCase Updates:
1. To update a case you need to ensure that you respond to messages with the generated tag and case number i.e. [HIVE NO:123].
2. Messages will be picked up and all observables extracted.
3. A default 'History' task is used to paste all information into the relevant case.

Does other stuff like filtering out your own defined observables, changing tag lines etc etc.

The File Structure is as follows;

- config.json 
 * Where you set up the mailbox's you wish to monitor and generate cases or alerts on.
 * Where you set up the internal email address settings that are used in other modules for sending emails to end users.
 * Location Attachments should be stored within the hive
 * The Hive Connection Details for connecting to the hive instance including api key
 * What the autocreate tag should be within the hive to detect that this is an auto-generated case or alert.
 * What new tag gets assigned when a case or alert is updated.
 * Search Attributes that will determine what modules are run based on certain criteria of the emails within the inbox and what is generated, an alert or a case.
 * Observables that should be removed from each case, You would want to remove the mailbox itselfs email so that all your cases don't correlate on this.

- settings.py
This is used purely to store the contents of the configuration file in memory so that all modules can access these variables
 * stored_hive_address=[] - Location of The Hive Instance.
 * stored_api_key=[] - API Key of The Hive.
 * stored_attachment_location=[] - Location Attachments should be stored once processed.
 * stored_auto_create_tag=[] - What tag is assigned to an alert or case generated using this script.
 * stored_update_tag=[] - What tag is assigned to an alert or case that is UPDATED using this script.
 * stored_internal_email=[] - The Internal email that will be used for email corrospendence.
 * stored_own_domain=[] - The domain of our own email addresses.
 * stored_def_recipient=[] - The user that recieves a copy of all emails.
 * stored_security_recipients=[]
 * stored_email_tag_line=[]
 * stored_remove_email_observables=[]
 * stored_remove_file_observables=[]
 * stored_remove_url_observables=[]
 * stored_remove_file_attachments=[]

- create_alert.py
This python script utilises the stored hive address and stored hive api key within the settings file to create a new case. It utilises thehiveAPI module to create an alert in the hive.

- 
