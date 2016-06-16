#######################################################
#                                                     #
# Name        : cited_refs.py                         #
# Date        : 06/13/2016                            #
# Description : Program to extract all the Cited      #
#               Cited references results              #
# Input File  : cited_ref.txt                         #
# Output File : cited_ref_result.txt                  #
#               cited_ref_page.txt                    #
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

def open_url(src_DOI, src_AN, ref_url):
    #f = urllib.urlopen(ref_url)
    f = br.open(ref_url)
    rsp = f.read()
    print(rsp)
    #### Beautifulsoup
    soup = BeautifulSoup(rsp, "html.parser")
    try:
        print("In try")
        result = soup.find('span', id="trueFinalResultCount")
        total_count = getValue(result.contents)
        print("Number of search results: %s" % (total_count))
        
        search_count = soup.find('span', id='pageCount.top')
        page_count = getValue(search_count.contents)
        print("Number of search pages: %s" % (page_count))
        
        if int(page_count) > 1:
            print("page count > 1")
            page_links = soup.find('a', {'class' : 'paginationNext', 'title' : 'Next Page'})
            page_link = page_links['href']
            page_link = page_link[:len(page_link)-1]
            i=1
            #while i <= 2:
            while i <= int(page_count):
                print(str(i) + "|" + page_link + str(i))
                print(str(i) + "|" + page_link + str(i), file=page_log)
                new_url = page_link + str(i)
                p = br.open(new_url)
                page_rsp = p.read()
                soup = BeautifulSoup(page_rsp, "html.parser")
                div_tags = soup.find_all('div', {'class' : "search-results-item"})
                print(div_tags)
                for div in div_tags:
                    try:
                        ref = div.find('a', {'class' : "smallV110"})['href'] 
                        print(ref)
                        link = "http://apps.webofknowledge.com" + ref
                    except TypeError:
                        link = "No link"
                    try:
                        span = div.find('span', {'class' : "reference-title"})
                        title = getValue(span.value.contents)
                    except AttributeError:
                        title = "Title: [not available]"
                    print(link)
                    print(title)
                    print(str(i) + "|" + src_DOI + "|" + src_AN + "|" + title + "|" + link)
                    print(str(i) + "|" + src_DOI + "|" + src_AN + "|" + title + "|" + link, file=result_log)
                br.back()
                i+=1
        elif int(page_count) == 1:
            print("page count == 1")
            print("1|" + ref_url)
            print("1|" + ref_url, file=page_log)
            div_tags = soup.find_all('div', {'class' : "search-results-item"})
            print(div_tags)
            for div in div_tags:
                try:
                    ref = div.find('a', {'class' : "smallV110"})['href']
                    print(ref)
                    link = "http://apps.webofknowledge.com" + ref
                except TypeError:
                    link = "No link"
                try:
                    span = div.find('span', {'class' : "reference-title"})
                    title = getValue(span.value.contents)
                except AttributeError:
                    title = "Title: [not available]"
                print(link)
                print(title)
                print("1|" + src_DOI + "|" + src_AN + "|" + title + "|" + link)
                print("1|" + src_DOI + "|" + src_AN + "|" + title + "|" + link, file=result_log)
    except AttributeError:
        print("1|" + "None of the Cited Articles are in your subscription", file=page_log)
        print("1|" + src_DOI + "|" + src_AN + "||" + "None of the Cited Articles are in your subscription", file=result_log)
    f.close()

br = mechanize.Browser()
in_file = "/home/usha/python/log/cited_ref.txt"
page_file ="/home/usha/python/log/cited_ref_page.txt"
page_log = open(page_file, "a")
result_file = "/home/usha/python/log/cited_ref_result.txt"
result_log = open(result_file, "a")

for line in file(in_file, "r"):
    print(line)
    src_DOI = line.split('|')[0]
    src_AN  = line.split('|')[1]
    cited_ref_url = line.split('|')[2]
    if cited_ref_url.strip()!= "No cited reference":
        open_url(src_DOI, src_AN, cited_ref_url)

page_log.close()
result_log.close()
