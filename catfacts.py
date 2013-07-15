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
import fact_scraper

now = datetime.datetime.now()
originalnow = now

gmail_user = "" ### YOUR GMAIL ACCOUNT HERE ### 
gmail_pwd = "" ### YOUR PASSWORD HERE ### 

    
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
msg_bdy = ""
msg_subj = "CAT FACT WOOOOO" ### YOUR SUBJECT HERE ###
email_addr = "" ### WHO YOU WANT TO SEND THE EMAILS TO ###
sent_this_minute = 0
prev_minute = now.minute
while(originalnow.minute <= now.minute and now.minute <= originalnow.minute + 1):
   if (sent_this_minute is 1) and (now.minute is originalnow.minute +2):
       break
   if now.second%2 is 0: #frequency -- every other second an email is sent
      msg_bdy = createMessage(num)
      msg_bdy += " trololol!"
      msg_subj += repr(now.second)
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
