#######################################################
#                                                     #
# Name        : extract_data.py                       #  
# Date        : 06/13/2016                            #  
# Description : Program to extract data based on the  #
#               results from search_pattern.py        #
# Input File  : result.txt                            #
# Output File : data.txt                              #
# Author      : Usha Boddeda                          #
#                                                     #
#######################################################

from __future__ import print_function
import urllib
import urllib2
import mechanize
import re
from lxml import html
from bs4 import BeautifulSoup
from functions import getValue
import sys, getopt
import datetime

if len(sys.argv) != 7:
    print("Usage: python extract_data.py -i <result_file> -o <data_file> -l <log file>")
    sys.exit(2)

pms = sys.argv[1:]
try:
   opts, args = getopt.getopt(pms,"i:o:l:")
except getopt.GetoptError:
   print("extract_data.py -i <result_file> -o <data_file> -l <log file>")
   sys.exit(2)
for opt, arg in opts:
   if opt == "-i":
      result_file = arg
   elif opt == "-o":
      data_file = arg
   elif opt == "-l":
      log_file = arg

log = open(log_file, "w")
print(datetime.datetime.now(), file=log)

print(result_file, file=log)
print(data_file, file=log)

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
    print("\n====================================\n", file=log)
    print(rsp, file=log)
    #### Beautifulsoup
    soup = BeautifulSoup(rsp, "html.parser")
    
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    
    #Code to extract Abstract, Keywords, Publisher, Categories/Classification, Document Information, DocumentType, Language
    div_tags = soup.find_all('div', {'class' : 'block-record-info'})
    for d in div_tags:
        print(d, file=log)
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

br=mechanize.Browser()
out = open(data_file, "w")
print("Extracting data....", file=log)
for cnt, line in enumerate(file(result_file, "r")):
    field1 = line.split('|')[0]
    url = line.split('|')[1]
    record = extract_data(url)
    print("%s%s" % (field1, record), file=out)

out.close()
cnt=cnt+1
print("Extracted %s records" % (cnt), file=log)
print(datetime.datetime.now(), file=log)
print("Success", file=log)
log.close()
