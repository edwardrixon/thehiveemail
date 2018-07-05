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

def linkParser(body):
    soup = BeautifulSoup(body, "lxml")
    links = soup.body('a')
#    email = '
#    phone = ''
#    final_links = []

#    for link in links:
#        if(link.get('href').find('mailto:') > -1):
#            final_links.append(link.extract())

    links = [link['href'] for link in soup('a') if 'href' in link.attrs]

    print(str(datetime.datetime.now())+"  Urls Extracted:",links)
    return list(set(links))

def emailParser(body):
    soup = BeautifulSoup(body, "lxml")
    mailtos = soup.select('a[href^=mailto]')
    emails = []

    for i in mailtos:
        if i.string != None:
            emails.append(i.string.encode('utf-8').strip())
    return list(set(emails))

def extractattachments(message):
    attachment_location=''.join(settings.stored_attachment_location[0])
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
   remove_observables = ''.join(settings.stored_remove_observables[0])

      body = part.get_payload(decode=True)
   print(str(datetime.datetime.now())+"  Running the url parser.")
   url_array=linkParser(body)
   print(str(datetime.datetime.now())+"  Running the email parser.")
   mail_array=emailParser(body)

   #This bit will now clean up the observables we dont care about.
   #Read in the skip this stuff
   #Read in the url array and mail_array and skip everythin not required
   #Pack whats left into the array and then return that

   return url_array, mail_array

def fix_html_body(charset,body):
   h = html2text.HTML2Text()
#   print ("Charset is:",charset)
   body = body.decode(charset, 'replace')
   body = h.handle(body)
   return body