#!/usr/bin/python
#######################################################
#                                                     #
# Name        : search_pattern.py                     #  
# Date        : 06/13/2016                            #  
# Description : Program to search the articles based  #
#               on data like journal, dates, etc      #
# Input File  : login.txt                             #
# Output File : result.txt                            #
# Author      : Usha Boddeda                          #
#                                                     #
#######################################################

from __future__ import print_function
import mechanize
import urllib2
from lxml import html
from bs4 import BeautifulSoup
from functions import getValue
import sys, getopt
import datetime

if len(sys.argv) != 9:
    print("Usage: python search_pattern.py -i <login file> -o <result_file> -j <journal> -l <log file>")
    sys.exit(2)

pms = sys.argv[1:]
try:
   opts, args = getopt.getopt(pms,"i:o:j:l:")
except getopt.GetoptError:
   print("search_pattern.py -i <login file> -o <result_file> -j <journal> -l <log file>")
   sys.exit(2)
for opt, arg in opts:
   if opt == "-i":
      login_file = arg
   if opt == "-o":
      result_file = arg
   elif opt == "-j":
      journal = arg
   elif opt == "-l":
      log_file = arg

log = open(log_file, "w")
print(datetime.datetime.now(), file=log)
print(result_file, file=log)
print(journal, file=log)

# Method to get search field based on choice
def search_field(choice):
    if choice == 1:
        return "TS"
    elif choice == 2:
        return "TI"
    elif choice == 3:
        return "AU"
    elif choice == 4:
        return "AI"
    elif choice == 5:
        return "ED"
    elif choice == 6:
        return "GP"
    elif choice == 7:
        return "SO"
    elif choice == 8:
        return "DO"
    elif choice == 9:
        return "PY"
    elif choice == 10:
        return "AD"

# Method to get search field from the user
def get_search_field():
    choice = 7
    field = search_field(choice)
    return field

# Select Range based on choice
def get_Range(choice):
    timespan = ""
    if choice == 1:
       timespan = "ALL"
    elif choice == 2:
       timespan = "Latest5Years"
    elif choice == 3:
       timespan = "YearToDate"
    elif choice == 4:
       timespan = "4week"
    elif choice == 5:
       timespan = "2week"
    elif choice == 6:
       timespan = "1week"
    return timespan

br=mechanize.Browser()
br.set_handle_robots(False)
line = file(login_file, "r")
url = line.readline()

page = br.open(url)
rsp = page.read()
print(rsp, file=log)
print("\n==================================\n", file=log)

#### Beautifulsoup
soup = BeautifulSoup(rsp, "html.parser")

select = soup.find('select', id="field_select_default")
opt_tags = select.find_all('option')

field = get_search_field()

# Steps to update the search based on given information
print(journal, file=log)
br.form = list(br.forms())[3]
control_select = br.form.find_control(type='select', name="value(select1)")

# loop through drop down list items to find match
for item in control_select.items:
    if item.name == field:
        item.selected = True
        break

text = journal
control_text = br.form.find_control(type='text', name="value(input1)")
control_text.value = text

# Steps to select timespan
while True:
    radio = 2
    div = soup.find('div', id="timespan")
    if int(radio) == 1:
        br.form.set_value(['Range Selection'], name="period")
        
        # Select range from drop down list
        ts_tags = div.find('input', {'name' : 'period'}).find_all('option')
        while True:
            print("\n=============================\n", file=log)
            for cnt, ts in enumerate(ts_tags):
                print("%s: %s" % (cnt+1, getValue(ts.contents)), file=log)
            print("\n=============================\n", file=log)
            choice = raw_input("Please select one of the above options: ")
            if int(choice) in [1, 2, 3, 4, 5, 6]:
                break
            else:
                print("Invalid choice, select again", file=log)
        timespan = get_Range(choice)

        control_select = br.form.find_control(type='select', name='range')
        # loop through drop down list items of timespan
        for each in control_select.items:
            if each.name == timespan:
                each.selected = True
                break
        break

    elif int(radio) == 2:
        br.form.set_value(['Year Range'], name="period")

        fromYear=1970
        toYear=2016
        control_start = br.form.find_control(type='select', name='startYear')
        # loop through drop down list of startYear
        for each in control_start.items:
            if int(each.name) == int(fromYear):
                each.selected = True
                break

        control_end = br.form.find_control(type='select', name='endYear')
        # loop through drop down list of endYear
        for each in control_end.items:
            if int(each.name) == int(toYear):
                each.selected = True
                break
        break

    else:
        print("Invalid option selected, choose again", file=log)

br.submit()
result = br.response().read()
soup = BeautifulSoup(result, 'html.parser')
print(result, file=log)
br.back()

result = soup.find('span', id="trueFinalResultCount")
total_count = getValue(result.contents)
print("Number of search results: %s" % (total_count), file=log)

search_count = soup.find('span', id='pageCount.top')
page_count = getValue(search_count.contents)
print("Number of search pages: %s" % (page_count), file=log)

if int(page_count) != 0:
    if int(page_count) == 1:
        page_links = soup.find('form', {'class' : 'pagination', 'name' : 'summary_navigation'})
        page_link = page_links['onsubmit'].split()[4]
        page_link = page_link[1:len(page_link)-2]
    elif int(page_count) > 1:
        page_links = soup.find('a', {'class' : 'paginationNext', 'title' : 'Next Page'})
        page_link = page_links['href']
        page_link = page_link[:len(page_link)-1]
    i=1
    result_log = open(result_file, "w")
    while i <= int(page_count):
        new_url = page_link + str(i)
        br.open(new_url)
        links_list = list(br.links(url_regex='full_record'))
        for index, each in enumerate(links_list):
            link = "http://apps.webofknowledge.com" + each.url
            print(each.text + "|" + link, file=result_log)
        br.back()
        i+=1

result_log.close()
print(datetime.datetime.now(), file=log)
print("Success", file=log)
log.close()
