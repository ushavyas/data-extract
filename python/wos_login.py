#######################################################
#                                                     #
# Name        : wos_login.py                          #  
# Date        : 06/13/2016                            #  
# Description : Program to login webofscience.com     #
# Input File  : None                                  #
# Output File : login.txt                             #
# Author      : Usha Boddeda                          #
#                                                     #
#######################################################

from __future__ import print_function
import mechanize
from bs4 import BeautifulSoup
from functions import getValue
import sys, getopt
import datetime

if len(sys.argv) != 9:
    print("Usage: python wos_login.py -o <login file> -u <username> -p <password> -l <log file>")
    sys.exit(2)

pms = sys.argv[1:]
try:
   opts, args = getopt.getopt(pms,"o:u:p:l:")
except getopt.GetoptError:
   print("Usage: python wos_login.py -o <login file> -u <username> -p <password> -l <log file>")
   sys.exit(2)
for opt, arg in opts:
   if opt == "-o":
      login_file = arg
   if opt == "-u":
      username = arg
   elif opt == "-p":
      password = arg
   elif opt == "-l":
      log_file = arg

log = open(log_file, "w")
print(datetime.datetime.now(), file=log)

br = mechanize.Browser()

def wos_login(username, password):
    try:
        url="http://login.webofknowledge.com"
        response = br.open(url)
    
        br.form = list(br.forms())[0]
    
        for control in br.form.controls:
            if control.type == "text":
               control.value = username
            elif control.type == "password":
               control.value = password
            elif control.type == "submit":
               control.disabled=True
    
        br.submit()
        result = br.response().read()
        soup = BeautifulSoup(result, 'html.parser')

        next_url = soup.find('input', id='currUrl')['value']
        print(next_url, file=login)

        # Logout
        #br.follow_link(text='Log Out')
    except TypeError:
        get_error = soup.find('td', {'class' : "NEWwokErrorContainer SignInLeftColumn"})
        error = getValue(get_error.find('h2').contents)
        print("Error: %s" % (error), file=log)
        next = 'y'
        if next not in ['y', 'Y']:
            print("Exiting", file=log)
        else:
            print("Closing other login session..", file=log)
            next_url = get_error.p.a['href']
            print(next_url, file=login)

login = open(login_file, "w")
wos_login(username, password)
print("You are logged in successfully", file=log)
login.close()
print(datetime.datetime.now(), file=log)
print("Success", file=log)
log.close()
