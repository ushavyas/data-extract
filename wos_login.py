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

br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
#br.set_handle_robots(False)   # ignore robots
#br.set_handle_refresh(False)  # can sometimes hang without this
#br.addheaders =("User-Agent", "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT")

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
        print("Error: %s" % (error))
        next = raw_input("%s (y/n)? : " % getValue(get_error.p.a.contents))
        #next = 'y'
        if next not in ['y', 'Y']:
            print("Exiting")
        else:
            print("Closing other login session..")
            next_url = get_error.p.a['href']
            print(next_url, file=login)

username = raw_input("Enter Username: ")
password = raw_input("Enter Password: ")
login_file = "/home/usha/python/log/login.txt"
login = open(login_file, "w")
wos_login(username, password)
print("You are logged in successfully")
