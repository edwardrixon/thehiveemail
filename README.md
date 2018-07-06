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

