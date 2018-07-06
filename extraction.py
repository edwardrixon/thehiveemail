#!/usr/bin/env python

from bs4 import BeautifulSoup
import HTMLParser
import quopri
import mailbox
import os
import email
import html2text 
import datetime
import chardet
import settings
import sys

def process_observables(test_item,test_type):

    if test_type=="url":
	remove_observables=settings.stored_remove_url_observables
    elif test_type=="email":
	remove_observables=settings.stored_remove_email_observables
    elif test_type=="file":
        remove_observables=settings.stored_remove_file_observables
    elif test_type=="attachments":
	remove_observables=settings.stored_remove_file_attachments
    else:
	print(str(datetime.datetime.now())+"  Incorrect test type passed through:"+test_type)
    
    final_items=[]

    #Now to go through and remove any that are to be ignored
    for link in test_item:
        i=0
        for i in range(len(remove_observables)+1):
                if remove_observables[0][i] not in link:
                        final_items.append(link)
                else:
                        break

    print(str(datetime.datetime.now())+"  Items Extracted:",final_items)
    return list(set(final_items))



def linkParser(body,test_type):
    soup = BeautifulSoup(body, "lxml")

    temp_link = []
    final_links = []
    email_links = []

    #Use the test type to determine which data to keep from the html either 'email' or 'url'

    for link in soup.find_all('a',href=True):
	url=link['href']

        if(url.find('mailto:') > -1):
    	    if test_type=="email":
            	temp_link.append(url)
        #elif(url.find('tel:') > -1):
        else:
            if test_type=="url":
		temp_link.append(url)


    final_links=process_observables(temp_link,test_type)
    return list(set(final_links))

def extractattachments(message):
    attachment_location=''.join(settings.stored_attachment_location[0])
    remove_observables = ''.join(settings.stored_remove_file_attachments[0])

    print(str(datetime.datetime.now())+"  Starting attachment extraction.") 
    pathList=""

    if message.is_multipart():
      
        pathList = []

        for part in message.walk():
            if part.get('Content-Disposition') is not None:      
                if part.get_content_maintype() == 'multipart': 
                    save_path = attachment_location
                    filename = part.get_filename()
                    print(str(datetime.datetime.now())+"  Extracting File:"+str(filename))
                    completePath = os.path.join(save_path, filename)
                    pathList.append(completePath)
#                   print (completePath)
                    fb = open(completePath,'wb')
        
                    fb.write(part.get_payload(decode=True))
                    fb.close()
                    return pathList
            else:
                print("Not Multipart...bypassing")
                pathList=""
    return pathList

def extractbody(email_message):

#Need to cater for multiple bits of a html part
    url_array=""
    mail_array=""

################################################################################################################
    if email_message.is_multipart():
       print(str(datetime.datetime.now())+"  Multipart message detected.")

       url_array=""
       mail_array=""

       body = []
       for part in email_message.walk():
          print(str(datetime.datetime.now())+"  Content type is "+str(part.get('Content-Disposition')))
          print(str(datetime.datetime.now())+"  Main Email type detected as "+part.get_content_type())
          if part.get_content_charset() is None: 
    
            charset = chardet.detect(str(part))['encoding']
            print(str(datetime.datetime.now())+"  Content charset detected as "+charset)
            
          else:
            charset = part.get_content_charset()
            print(str(datetime.datetime.now())+"  Content charset detected as "+charset)

          if part.get_content_maintype() == 'multipart': 
            print(str(datetime.datetime.now())+"  Multipart email is type "+part.get_content_type())
            
            continue
          #print(str(datetime.datetime.now())+"  Email type detected as "+part.get_content_type())
          if part.get_content_type() == "text/html" and 'attachment' not in str(part.get('Content-Disposition')):
             print (str(datetime.datetime.now())+"  Extracting text/html body.")
             
             #This will build the array for a multipart message
             if 'attachment' not in str(part.get('Content-Disposition')):
                body.append(process_html(part)) 
             url_array, mail_array = html_observables(part)
#             body = u''.join((body)).encode('utf-8').strip()
          elif part.get_content_type() == "text/plain" and 'attachment' not in str(part.get('Content-Disposition')):
             print (str(datetime.datetime.now())+"  Extracting text/plain body.") 
             body.append(part.get_payload(decode=True))

    else:
       print(str(datetime.datetime.now())+"  Single (non-multipart) message detected.")

       if email_message.get_content_type() == "text/html":
           print (str(datetime.datetime.now())+"  Extracting text/html body.") 
           if 'attachment' not in str(email_message.get('Content-Disposition')):
              body=process_html(email_message)
           else:
              print("its an attachment - skip it")
           url_array, mail_array = html_observables(email_message)

       elif email_message.get_content_type() == "text/plain":
           print (str(datetime.datetime.now())+"  Extracting text/plain body.")
           if 'attachment' not in str(email_message.get('Content-Disposition')):
              body = email_message.get_payload(decode=True)
           else:
              print("its an attachment - skip it")

    #This works but errors on the exception and wont send the email due to a UnicodeEncodeError
    try:
         
       converted = [test.encode("utf8", "ignore") for test in body]
    except UnicodeDecodeError:
       converted = [test.decode("utf8", "ignore") for test in body]
       #converted = ''.join(map(str,body))
    converted2 = ''.join(converted)
    #converted2=unicode(converted, encoding="utf-8", errors="ignore")
    #print("CONVERTED:",converted2)

    body = converted2
    return body, url_array, mail_array

def process_html(part):
   charset = part.get_content_charset('iso-8859-1')
   body = part.get_payload(decode=True)
   body = fix_html_body(charset,body)
   return body

       
def html_observables(part):
    #Read in the list of observables

    body = part.get_payload(decode=True)
    print(str(datetime.datetime.now())+"  Running the url parser.")
    url_array=linkParser(body,"url")
    print(str(datetime.datetime.now())+"  Url items Extracted:",url_array)
    print(str(datetime.datetime.now())+"  Running the email parser.")
    mail_array=linkParser(body,"email")
    print(str(datetime.datetime.now())+"  Email items Extracted:",mail_array)
    #sys.exit(0)

    return url_array, mail_array

def fix_html_body(charset,body):
   h = html2text.HTML2Text()
#   print ("Charset is:",charset)
   body = body.decode(charset, 'replace')
   body = h.handle(body)
   return body
