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
#import mailparser 

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

def extractattachments(message,attachment_location):
   print(str(datetime.datetime.now())+"  Starting attachment extraction.") 
   if message.is_multipart():
      
      pathList = []

      for part in message.walk():
         if part.get_content_maintype() == 'multipart': continue
         if part.get('Content-Disposition') is None: continue

         save_path = attachment_location
         filename = part.get_filename()
         print(str(datetime.datetime.now())+"  Extracting File:"+str(filename))
         completePath = os.path.join(save_path, filename)
         pathList.append(completePath)
#         print (completePath)
         fb = open(completePath,'wb')
        
         fb.write(part.get_payload(decode=True))
         fb.close()
         return pathList
   else:
      print("Not Multipart...bypassing")
      pathList=""
   return pathList

def extractbody(email_message):
    attachment_location=''.join(settings.stored_attachment_location[0])
#Need to cater for multiple bits of a html part
    url_array=""
    mail_array=""

################################################################################################################
    if email_message.is_multipart():
       print(str(datetime.datetime.now())+"  Multipart message detected.")
       html = None #NEW
       text = "" #NEW

       url_array=""
       mail_array=""

       body = []
       for part in email_message.walk():
          cdispo = str(part.get('Content-Disposition'))
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
             print("ITS AN ATTACHMENT SO ITS BEEN SKIPPED")
             file_array = extractattachments(email_message,attachment_location)

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
    print("BODY2:",str(converted))
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
   charset = part.get_content_charset('iso-8859-1')
   body = part.get_payload(decode=True)
   print("Running the url parser")
   url_array=linkParser(body)
   print("Running the email parser")
   mail_array=emailParser(body)
   return url_array, mail_array

def fix_html_body(charset,body):
   h = html2text.HTML2Text()
#   print ("Charset is:",charset)
   body = body.decode(charset, 'replace')
   body = h.handle(body)
   return body
   