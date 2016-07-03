#######################################################
#                                                     #
# Name        : link_refs.py                          #  
# Date        : 06/13/2016                            #  
# Description : Program to extract Cited references & #
#               Citing references links               #
# Input File  : result.txt                            #
# Output File : cited_ref.txt, citing_ref.txt         #
# Author      : Usha Boddeda                          #
#                                                     #
#######################################################

from __future__ import print_function
import urllib
import urllib2
import re
from lxml import html
from bs4 import BeautifulSoup
from functions import getValue
import sys, getopt
import datetime

if len(sys.argv) != 9:
    print("Usage: python link_refs.py -i <result_file> -1 <cited_ref_file> -2 <citing_ref_file> -l <log file>")
    sys.exit(2)

pms = sys.argv[1:]
try:
   opts, args = getopt.getopt(pms,"i:1:2:l:")
except getopt.GetoptError:
   print("Usage: python link_refs.py -i <result_file> -1 <cited_ref_file> -2 <citing_ref_file> -l <log file>")
   sys.exit(2)
for opt, arg in opts:
   if opt == "-i":
      result_file = arg
   elif opt == "-1":
      cited_ref_file = arg
   elif opt == "-2":
      citing_ref_file = arg
   elif opt == "-l":
      log_file = arg

log = open(log_file, "w")
print(datetime.datetime.now(), file=log)

cited_ref_out = open(cited_ref_file, "w")
citing_ref_out = open(citing_ref_file, "w")
for line in file(result_file, "r"):
    DOI=""
    AN=""
    cited_ref_cnt=0
    citing_ref_cnt=0
    url = line.split('|')[1]
    f = urllib.urlopen(url)
    rsp = f.read()
    print(rsp, file=log)
    #### Beautifulsoup
    soup = BeautifulSoup(rsp, "html.parser")
    p_tags = soup.find_all('p', {'class' : 'FR_field'})
    #p_tags = p_tags[1:]
    for p in p_tags:
        try:
            span = getValue(p.span.contents)
            span = span.split(':')[0]
            if span == "DOI":
                DOI=getValue(p.value.contents)
            elif span == "Accession Number":
                AN=getValue(p.value.contents)
            elif span == "Cited References in Web of Science Core Collection":
                cited_ref_cnt=getValue(p.b.contents)
            elif span == "Times Cited in Web of Science Core Collection":
                citing_ref_cnt=getValue(p.b.contents)
        except AttributeError:
            pass
    print("DOI:%s AN:%s CNT1:%s CNT2:%s" % (DOI, AN, cited_ref_cnt, citing_ref_cnt), file=log)
    div = soup.find('div', {'class' : 'block-text-content'})
    print("\n===========================\n", file=log)
    print(div, file=log)
    a = div.find_all('a')
    print("\n===========================\n", file=log)
    print(a, file=log)
    print("\n===========================\n", file=log)
    print("\nCited Ref Cnt: %s" % (cited_ref_cnt), file=log)
    print("\nCiting Ref Cnt: %s" % (citing_ref_cnt), file=log)
    cited_ref_cnt = str(cited_ref_cnt).replace(',','')
    citing_ref_cnt = str(citing_ref_cnt).replace(',','')
    if int(cited_ref_cnt) > 0:
        cited_ref_url = div.find('a', {'title' : re.compile('View this record.*.bibliography')})['href']
        cited_ref_url = "http://apps.webofknowledge.com/" + cited_ref_url
        print("%s|%s|%s" % (DOI, AN, cited_ref_url), file=cited_ref_out)
    else:
        print("%s|%s|No cited reference" % (DOI, AN), file=cited_ref_out)
    if int(citing_ref_cnt) > 0:
        citing_ref_url = div.find('a', {'title' : "View all of the articles that cite this one"})['href']
        citing_ref_url = "http://apps.webofknowledge.com" + citing_ref_url
        print("%s|%s|%s" % (DOI, AN, citing_ref_url), file=citing_ref_out)
    else:
        print("%s|%s|No citing reference" % (DOI, AN), file=citing_ref_out)
    f.close()

cited_ref_out.close()
citing_ref_out.close()
print(datetime.datetime.now(), file=log)
print("Success", file=log)
log.close()
