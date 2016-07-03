#######################################################
#                                                     #
# Name        : cited_refs.py                         #
# Date        : 06/13/2016                            #
# Description : Program to extract  all the Cited    #
#               references results, corresponding data#
#               and connecting information            #
# Input File  : cited_ref.txt                         #
# Output File : cited_ref_result.txt                  #
#               cited_ref_data.txt                    #
#               cited_ref_link.txt                    #
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
from functions import extract_data
import sys, getopt
import datetime

if len(sys.argv) != 11:
    print("Usage: python cited_refs.py -i <cited_ref_file> -1 <cited_ref_res_file> -2 <cited_ref_dat_file> -3 <cited_ref_link_file> -l <log file>")
    sys.exit(2)

pms = sys.argv[1:]
try:
   opts, args = getopt.getopt(pms,"i:1:2:3:l:")
except getopt.GetoptError:
   print("Usage: python cited_refs.py -i <cited_ref_file> -1 <cited_ref_res_file> -2 <cited_ref_dat_file> -3 <cited_ref_link_file> -l <log file>")
   sys.exit(2)
for opt, arg in opts:
   if opt == "-i":
      cited_ref_file = arg
   elif opt == "-1":
      cited_ref_res_file = arg
   elif opt == "-2":
      cited_ref_dat_file = arg
   elif opt == "-3":
      cited_ref_link_file = arg
   elif opt == "-l":
      log_file = arg

log = open(log_file, "w")
print(datetime.datetime.now(), file=log)

def getCitedRefData(cited_line):
    rec_num = cited_line.split('|')[0]
    src_doi = cited_line.split('|')[1]
    src_an = cited_line.split('|')[2]
    field1 = cited_line.split('|')[3]
    url = cited_line.split('|')[4]
    if url.strip() != "No link" or url.strip() != "None of the Cited Articles are in your subscription":
        try:
            record = extract_data(url)
            print(record, file=log)
            dst_doi = record.split('|')[11]
            dst_an = record.split('|')[20]
            link_rec = "|".join([rec_num, src_doi, src_an, dst_doi, dst_an])
        except IOError:
            record = "|||||||||||||||||||||||||"
            link_rec = "|".join([rec_num, src_doi, src_an, "", ""])
    else:
        record = "|No link for data||||||||||||||||||||||||"
        link_rec = "|".join([rec_num, src_doi, src_an, "", ""])
    print("%s%s" % (field1, record), file=data_out)
    print(link_rec, file=link_out)

def open_url(src_DOI, src_AN, ref_url):
    #f = urllib.urlopen(ref_url)
    f = br.open(ref_url)
    rsp = f.read()
    print(rsp, file=log)
    #### Beautifulsoup
    soup = BeautifulSoup(rsp, "html.parser")
    try:
        result = soup.find('span', id="trueFinalResultCount")
        total_count = getValue(result.contents)
        print("Number of search results: %s" % (total_count), file=log)
        
        search_count = soup.find('span', id='pageCount.top')
        page_count = getValue(search_count.contents)
        print("Number of search pages: %s" % (page_count), file=log)
    
        if int(page_count) == 1:
            print("1|" + ref_url, file=log)
            div_tags = soup.find_all('div', {'class' : "search-results-item"})
            print(div_tags, file=log)
            for div in div_tags:
                try:
                    ref = div.find('a', {'class' : "smallV110"})['href']
                    print(ref, file=log)
                    link = "http://apps.webofknowledge.com" + ref
                except TypeError:
                    link = "No link"
                try:
                    span = div.find('span', {'class' : "reference-title"})
                    title = getValue(span.value.contents)
                    print(title, file=log)
                except AttributeError:
                    title = "Title: [not available]"
                print("1|" + src_DOI + "|" + src_AN + "|" + title + "|" + link, file=log)
                print("1|" + src_DOI + "|" + src_AN + "|" + title + "|" + link, file=result_log)
                cited_line = "1|" + src_DOI + "|" + src_AN + "|" + title + "|" + link
                getCitedRefData(cited_line)
        if int(page_count) > 1:
            page_links = soup.find('a', {'class' : 'paginationNext', 'title' : 'Next Page'})
            page_link = page_links['href']
            page_link = page_link[:len(page_link)-1]
            i=1
            #while i <= 2:
            while i <= int(page_count):
                print(str(i) + "|" + page_link + str(i), file=log)
                new_url = page_link + str(i)
                p = br.open(new_url)
                page_rsp = p.read()
                soup = BeautifulSoup(page_rsp, "html.parser")
                div_tags = soup.find_all('div', {'class' : "search-results-item"})
                print(div_tags, file=log)
                for div in div_tags:
                    try:
                        ref = div.find('a', {'class' : "smallV110"})['href']
                        print(ref, file=log)
                        link = "http://apps.webofknowledge.com" + ref
                    except TypeError:
                        link = "No link"
                    try:
                        span = div.find('span', {'class' : "reference-title"})
                        title = getValue(span.value.contents)
                        print(title, file=log)
                    except AttributeError:
                        title = "Title: [not available]"
                    print(str(i) + "|" + src_DOI + "|" + src_AN + "|" + title + "|" + link, file=log)
                    print(str(i) + "|" + src_DOI + "|" + src_AN + "|" + title + "|" + link, file=result_log)
                    cited_line = str(i) + "|" + src_DOI + "|" + src_AN + "|" + title + "|" + link
                    getCitedRefData(cited_line)
                br.back()
                i+=1
    except AttributeError:
        print("1|" + src_DOI + "|" + src_AN + "||" + "None of the Cited Articles are in your subscription", file=result_log)
        cited_line = "1|" + src_DOI + "|" + src_AN + "||" + "None of the Cited Articles are in your subscription"
        link = "None of the Cited Articles are in your subscription"
        getCitedRefData(cited_line)
    f.close()

br = mechanize.Browser()
result_log = open(cited_ref_res_file, "w")
data_out = open(cited_ref_dat_file, "w")
link_out = open(cited_ref_link_file, "w")

for line in file(cited_ref_file, "r"):
    print(line, file=log)
    src_DOI = line.split('|')[0]
    src_AN  = line.split('|')[1]
    cited_ref_url = line.split('|')[2]
    if cited_ref_url.strip() != "No cited reference":
        open_url(src_DOI, src_AN, cited_ref_url)

result_log.close()
data_out.close()
link_out.close()
print(datetime.datetime.now(), file=log)
print("Success", file=log)
log.close()
