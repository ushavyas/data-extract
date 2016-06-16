#######################################################
#                                                     #
# Name        : functions.py                          #
# Date        : 06/13/2016                            #
# Description : Python functions to be reused in      #
#               other programs                        #
# Author      : Usha Boddeda                          #
#                                                     #
#######################################################

from __future__ import print_function
import urllib
import urllib2
import httplib
import mechanize
import time
from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver
import re

# Method to return value from html contents
def getValue(tag):
    mystr = str(tag)
    return mystr[3:len(mystr)-2]

def have_internet():
    conn = httplib.HTTPConnection("www.google.com")
    while True:
        try:
            conn.request("HEAD", "/")
            return True
        except:
            time.sleep(10)

def session_check1(soup, log):
    print("1111111111111111111111", file=log)
    get_error = soup.find('td', {'class' : "NEWwokErrorContainer SignInLeftColumn "})
    print(get_error, file=log)
    print("1111111111111111111111", file=log)
    if get_error == "None":
        return True
    print("1111111111111111111111", file=log)
    error = getValue(get_error.find('h2').contents)
    print(error, file=log)
    next_url = get_error.p.p.a['href']
    print(next_url, file=log)
    br = mechanize.Browser()
    next = br.open(next_url)
    next_rsp = next.read()
    print("\n+++++++++++++++++++++++\n", file=log)
    print(next_rsp)
    username="ushapraveena.boddeda@sjsu.edu"
    password="Mbd@0711"

    br.form = list(br.forms())[0]
    print(br.form)

    for control in br.form.controls:
        if control.type == "text":
           control.value = username
        elif control.type == "password":
           control.value = password
    print(br.form)

    br.click(type="image")

def session_check(soup, log):
    print("1111111111111111111111", file=log)
    get_error = soup.find('td', {'class' : "NEWwokErrorContainer SignInLeftColumn "})
    print(get_error, file=log)
    print("1111111111111111111111", file=log)
    if get_error == "None":
        return True
    print("1111111111111111111111", file=log)
    error = getValue(get_error.find('h2').contents)
    print(error, file=log)
    next_url = get_error.p.p.a['href']
    print(next_url, file=log)
    br = webdriver.Firefox()
    br.get(next_url)
    username="ushapraveena.boddeda@sjsu.edu"
    password="Mbd@0711"

    userinput = br.find_element_by_name('username')
    userinput.send_keys(username)
    pswdinput = br.find_element_by_name('password')
    pswdinput.send_keys(password)

    button = br.find_element_by_name('image')
    button.click()
    print(br.current_url, file=log)
    cur_url=br.current_url
    cr=mechanize.Browser()
    next_rsp = cr.open(cur_url)
    result = next_rsp.read()
    print(result, file=log)
    soup1 = BeautifulSoup(result, 'html.parser')
    get_error = soup1.find('td', {'class' : "NEWwokErrorContainer SignInLeftColumn"})
    print(get_error, file=log)
    error = getValue(get_error.find('h2').contents)
    print("Error: %s" % (error), file=log)
    print("Closing other login session..")
    new_url = get_error.p.a['href']
    cr.open(new_url)
    
    print(br.title, file=log)
    print(next_rsp, file=log)
    br.close()

def extract_data(data_url):
    field1=""
    field2=""
    field3=""
    field4=""
    field5=""
    field6=""
    field7=""
    field8=""
    field9=""
    field10=""
    field11=""
    field12=""
    field13=""
    field14=""
    field15=""
    field16=""
    field17=""
    field18=""
    field19=""
    field20=""
    field21=""
    field22=""
    field23=""
    field24=""
    field25=""
    field26=""
    f = urllib.urlopen(data_url)
    rsp = f.read()
    #### Beautifulsoup
    soup = BeautifulSoup(rsp, "html.parser")
    
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    
    #Code to extract Abstract, Keywords, Publisher, Categories/Classification, Document Information, DocumentType, Language
    div_tags = soup.find_all('div', {'class' : 'block-record-info'})
    for d in div_tags:
        try:
            title = getValue(d.div.contents)
            if title == "Abstract":
                field14=getValue(d.p.contents)
            elif title == "Keywords":
                a_tags = d.p.find_all('a', {'title' : "Find more records by this keywords plus"})
                for a in a_tags:
                    field15=field15 + ", " + getValue(a.contents)
                field15=field15[2:]
            elif title == "Publisher":
                field16=getValue(d.p.value.contents)
            elif title == "Categories / Classification":
                field18=d.p.get_text().split(':')[1]
            elif title == "Document Information":
                for doc in d.find_all('p'):
                    span = getValue(doc.span.contents)
                    value = doc.get_text().split(':')[1]
                    if span == "Document Type:":
                        field19=value
                    elif span == "Language:":
                        field20=value
        except AttributeError:
            pass
    
    #Code to extract Author, Volume, Issue, Pages, DOI, Published Date, ISSN, Research Domain, Accession Number, eISSN, IDS Number
    
    p_tags = soup.find_all('p', {'class' : 'FR_field'})
    #p_tags = p_tags[1:]
    for p in p_tags:
        try:
            span = getValue(p.span.contents)
            span = span.split(':')[0]
            if span == "By":
                a_tags = p.find_all('a', {'title' : "Find more records by this author"})
                for a in a_tags:
                    field2=field2 + "; " + getValue(a.contents)
                    try:
                        field3=field3 + "; " + a.next_sibling.split('(')[1].split(')')[0].strip()
                    except IndexError:
                        pass
                field2=field2[2:]
                field3=field3[2:]
            elif span == "Reprint Address":
                field4=p.span.next_sibling.split('(')[0].strip()
                field5=p.find('td', {'class': 'fr_address_row2'}).contents[0]
            elif span == "Addresses":
                tr_tags = p.find_all('tr')
                for tr in tr_tags:
                    try:
                        field6=field6 + "; " + getValue(tr.preferred_org.contents)
                    except AttributeError:
                        pass
                field6=field6[2:]
                a_tags = p.find_all('a', {'name': re.compile("addressWOS:*")})
                for a in a_tags:
                    field7=field7 + "; " + getValue(a.contents)
                field7=field7[2:]
            elif span == "E-mail Addresses":
                a_tags = p.find_all('a')
                for a in a_tags:
                    field8=field8 + "; " + getValue(a.contents)
                field8=field8[2:]
            elif span == "Volume":
                field9=getValue(p.value.contents)
            elif span == "Issue":
                field10=getValue(p.value.contents)
            elif span == "Pages":
                field11=getValue(p.value.contents)
            elif span == "DOI":
                field12=getValue(p.value.contents)
            elif span == "Published":
                field13=getValue(p.value.contents)
            elif span == "ISSN":
                field22=getValue(p.value.contents)
            elif span == "Research Domain ":
                field17=getValue(p.value.contents)
            elif span == "Accession Number":
                field21=getValue(p.value.contents)
            elif span == "eISSN":
                field23=getValue(p.value.contents)
            elif span == "IDS Number":
                field24=getValue(p.value.contents)
            elif span == "Cited References in Web of Science Core Collection":
                field25=getValue(p.a.b.contents)
            elif span == "Times Cited in Web of Science Core Collection":
                field26=getValue(p.b.contents)
        except AttributeError:
            pass

    record = "|".join([field1, field2, field3, field4, field5, field6, field7, field8, field9, field10, field11, field12, field13, field14, field15, field16, field17, field18, field19, field20, field21, field22, field23, field24, field25, field26])
    f.close()
    return record

def extract_data_old(data_url):
    field1=""
    field2=""
    field3=""
    field4=""
    field5=""
    field6=""
    field7=""
    field8=""
    field9=""
    field10=""
    field11=""
    field12=""
    field13=""
    field14=""
    field15=""
    field16=""
    field17=""
    field18=""
    field19=""
    field20=""
    f = urllib.urlopen(data_url)
    rsp = f.read()
    #### Beautifulsoup
    soup = BeautifulSoup(rsp, "html.parser")
    
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    
    div_tags = soup.find_all('div', {'class' : 'block-record-info'})
    for d in div_tags:
        try:
            title = getValue(d.div.contents)
            if title == "Abstract":
                field8=getValue(d.p.contents)
            elif title == "Keywords":
                a_tags = d.p.find_all('a', {'title' : "Find more records by this keywords plus"})
                for a in a_tags:
                    field9=field9 + ", " + getValue(a.contents)
                field9=field9[2:]
            elif title == "Publisher":
                field10=getValue(d.p.value.contents)
            elif title == "Categories / Classification":
                field12=d.p.get_text().split(':')[1]
            elif title == "Document Information":
                for doc in d.find_all('p'):
                    span = getValue(doc.span.contents)
                    value = doc.get_text().split(':')[1]
                    if span == "Document Type:":
                        field13=value
                    elif span == "Language:":
                        field14=value
        except AttributeError:
            pass
    
    #Code to extract Volume, Issue, Pages, DOI, Published Date, ISSN, Research Domain, Accession Number, eISSN, IDS Number
    
    p_tags = soup.find_all('p', {'class' : 'FR_field'})
    #p_tags = p_tags[1:]
    for p in p_tags:
        try:
            span = getValue(p.span.contents)
            span = span.split(':')[0]
            if span == "By":
                a_tags = p.find_all('a', {'title' : "Find more records by this author"})
                for a in a_tags:
                    field2=field2 + "; " + getValue(a.contents)
                field2=field2[2:]
            elif span == "Volume":
                field3=getValue(p.value.contents)
            elif span == "Issue":
                field4=getValue(p.value.contents)
            elif span == "Pages":
                field5=getValue(p.value.contents)
            elif span == "DOI":
                field6=getValue(p.value.contents)
            elif span == "Published":
                field7=getValue(p.value.contents)
            elif span == "ISSN":
                field16=getValue(p.value.contents)
            elif span == "Research Domain ":
                field11=getValue(p.value.contents)
            elif span == "Accession Number":
                field15=getValue(p.value.contents)
            elif span == "eISSN":
                field17=getValue(p.value.contents)
            elif span == "IDS Number":
                field18=getValue(p.value.contents)
            elif span == "Cited References in Web of Science Core Collection":
                field19=getValue(p.a.b.contents)
            elif span == "Times Cited in Web of Science Core Collection":
                field20=getValue(p.b.contents)
        except AttributeError:
            pass
    
    record = "|".join([field1, field2, field3, field4, field5, field6, field7, field8, field9, field10, field11, field12, field13, field14, field15, field16, field17, field18, field19, field20])
    f.close()
    return record

def wos_login(username, password):
    login_file = "/home/usha/python/log/login.txt"
    login = open(login_file, "w")
    try:
        br = mechanize.Browser()
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
