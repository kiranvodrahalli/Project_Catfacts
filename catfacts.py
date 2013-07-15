# catfacts.py
# Author: Kiran Vodrahalli
# Last updated: 07/14/2013
# runs a cron job on sending emails (you can specify)
# by scraping from some website (default is about cats)
# no support yet for types of websites that are not list-based and simple

import re 
import bs4
import urllib2
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import datetime
import io 
import fact_scraper

now = datetime.datetime.now()
originalnow = now

### IMPORTANT ####
# In order to fill in the values for these variables, 
# make a file called "usr_options.txt"
# The format of the file is as follows:
# line1: gmail_user string (name of your gmail account)
# line2: gmail_pwd string (name of your gmail password)
# line3: email_addr string (name of receiver's email address)
# line4: msg_subj string (subject of email)
# line5: msg_bdy string (body of email)
#####################################################

# read the values off of "usr_options.txt"
usr_options = "usr_options.txt"
option_entries = []

usrf = open(usr_options)
for line in usrf:
  option_entries.append(line[:-1])


# put these into a separate file
gmail_user = option_entries[0] ### YOUR GMAIL ACCOUNT ### 
gmail_pwd = option_entries[1] ### YOUR PASSWORD ### 

# put these into a separate file 
email_addr = option_entries[2] ### WHO YOU WANT TO SEND THE EMAILS TO ###
msg_subj = option_entries[3] ### YOUR SUBJECT  ###
msg_bdy = option_entries[4] ### YOUR MESSAGE  ### 

    
mailServer = smtplib.SMTP("smtp.gmail.com", 587)
mailServer.ehlo()
mailServer.starttls()
mailServer.ehlo()
mailServer.login(gmail_user, gmail_pwd)

def mail(to, subject, text):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   mailServer.sendmail(gmail_user, to, msg.as_string())


url = "http://facts.randomhistory.com/interesting-facts-about-cats.html"  #to cat facts page
f = urllib2.urlopen(url)
html = f.read()

facts = fact_scraper.produceObjects(html, ['li'], "", [], False, "CAT_FACT")

def createMessage(factNum):
  return "CAT FACTS CONGRATULATES YOU!!! Here is your cat fact for the day! Voila: {0}".format(facts[factNum])
 

num = 0 # which fact
sent_this_minute = 0


prev_minute = now.minute
while(originalnow.minute <= now.minute and now.minute <= originalnow.minute + 1):
   if (sent_this_minute is 1) and (now.minute is originalnow.minute +2): #how long should the cron job run
       break
   if now.second%2 is 0: #frequency -- every other second an email is sent
      msg_bdy = createMessage(num)
      #msg_bdy += " trololol!" for the trollz out there 
      #msg_subj += repr(now.second) adds the seconds it's sent at to the message subject
      if sent_this_minute is 0:
          mail(email_addr, msg_subj, msg_bdy)
          num += 1
          print "send to: " + email_addr
          print "message title: " + msg_subj
          print "message subject: " + msg_bdy
          print now.minute
          print now.second
          print "\n"
         # sent_this_minute = 1
   now = datetime.datetime.now()
   if now.minute is not prev_minute:
        sent_this_minute = 0
        prev_minute = now.minute





mailServer.close()
