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
    print("\n=============================\n")
    print("Please select one of the options from below: (Example: To select 'Author', press 3 and Enter)")
    for cnt, opt in enumerate(opt_tags):
        print("%s : %s" % (cnt + 1, getValue(opt.contents)))
    print("\n=============================\n")
    
    choice = raw_input("Your option: ")
    #choice = 7
    field = search_field(choice)
    return field

# Method to update the search based on given information
def select_search(field):
    br.form = list(br.forms())[3]
    
    control_select = br.form.find_control(type='select', name="value(select1)")
    
    # loop through drop down list items to find match
    for item in control_select.items:
        if item.name == field:
            item.selected = True
            break
    
    text = raw_input("Enter text to search: ")
    #text = "academy of management journal"
    
    control_text = br.form.find_control(type='text', name="value(input1)")
    print("\n=============================\n")
    control_text.value = text

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

# Method to select timespan
def set_Timespan():
    while True:
        print("\n=============================\n")
        print("1. Range Selection")
        print("2. Year Range")
        radio = raw_input("Select an option for timespan: ")
        div = soup.find('div', id="timespan")
        if int(radio) == 1:
            br.form.set_value(['Range Selection'], name="period")
            
            # Select range from drop down list
            ts_tags = div.find('input', {'name' : 'period'}).find_all('option')
            while True:
                print("\n=============================\n")
                for cnt, ts in enumerate(ts_tags):
                    print("%s: %s" % (cnt+1, getValue(ts.contents)))
                print("\n=============================\n")
                choice = raw_input("Please select one of the above options: ")
                if int(choice) in [1, 2, 3, 4, 5, 6]:
                    break
                else:
                    print("Invalid choice, select again")
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
    
            from_sel = div.find('select', {'name' : 'startYear'}).find_all('option')
            from_start = from_sel[0]['value']
            from_end = from_sel[len(from_sel)-1]['value']
            to_sel = div.find('select', {'name' : 'endYear'}).find_all('option')
            to_start = to_sel[0]['value']
            to_end = to_sel[len(to_sel)-1]['value']
            startYear = int(raw_input("Please select the Start year between %s and %s: " % (from_start, from_end)))
            endYear   = int(raw_input("Please select the End year between %s and %s: " % (to_start, to_end)))
            #startYear=2010
            #endYear=2016
            control_start = br.form.find_control(type='select', name='startYear')
            # loop through drop down list of startYear
            for each in control_start.items:
                if each.name == startYear:
                    each.selected = True
                    break
    
            control_end = br.form.find_control(type='select', name='endYear')
            # loop through drop down list of endYear
            for each in control_end.items:
                if each.name == endYear:
                    each.selected = True
                    break
            break

        else:
            print("Invalid option selected, choose again")


br=mechanize.Browser()
br.set_handle_robots(False)
in_file = "/home/usha/python/log/login.txt"
line = file(in_file, "r")
url = line.readline()
#url = "http://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=3DnYEs3nu2hw57QsSs8&preferencesSaved="
print(url)

page = br.open(url)
rsp = page.read()
ex_file = "/home/usha/python/log/ex.txt"
ex_log = open(ex_file, 'w')
print(rsp, file=ex_log)
print("\n==================================\n", file=ex_log)
#page = html.fromstring(rsp)

#### Beautifulsoup
soup = BeautifulSoup(rsp, "html.parser")

# kill all script and style elements
'''for script in soup(["script", "style"]):
    script.extract()    # rip it out'''

select = soup.find('select', id="field_select_default")
opt_tags = select.find_all('option')

#while True:
field = get_search_field()
select_search(field)
set_Timespan()
#add = raw_input("Want to add another search field? (Y/N): ")
#add = 'n'
#if add not in ['Y', 'y']:
#    break

br.submit()
print("\n=============================\n")
result = br.response().read()
soup = BeautifulSoup(result, 'html.parser')
############
print(result, file=ex_log)
ex_log.close()
br.back()

result = soup.find('span', id="trueFinalResultCount")
total_count = getValue(result.contents)
print("Number of search results: %s" % (total_count))

search_count = soup.find('span', id='pageCount.top')
page_count = getValue(search_count.contents)
print("Number of search pages: %s" % (page_count))

page_links = soup.find('a', {'class' : 'paginationNext', 'title' : 'Next Page'})
page_link = page_links['href']
page_link = page_link[:len(page_link)-1]
i=1
page_file ="/home/usha/python/log/page.txt"
page_log = open(page_file, "w")
result_file = "/home/usha/python/log/result.txt"
result_log = open(result_file, "w")
#while i <= 2:
while i <= int(page_count):
    print(str(i) + "|" + page_link + str(i), file=page_log)
    new_url = page_link + str(i)
    br.open(new_url)
    links_list = list(br.links(url_regex='full_record'))
    for index, each in enumerate(links_list):
        link = "http://apps.webofknowledge.com" + each.url
        print(each.text + "|" + link, file=result_log)
    br.back()
    i+=1

page_log.close()
result_log.close()
