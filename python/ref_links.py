#######################################################
#                                                     #
# Name        : ref_links.py                          #
# Date        : 06/13/2016                            #
# Description : Program to convert link files into    #
#               excel sheets                          #
# Input File  : link.txt                              #
# Output File : links.xls                             #
# Author      : Usha Boddeda                          #
#                                                     #
#######################################################

from __future__ import print_function
import urllib
import urllib2
import xlsxwriter
from lxml import html
from bs4 import BeautifulSoup
import sys, getopt
import datetime

if len(sys.argv) != 7:
    print("Usage: python ref_links.py -i <link file> -o <link xls file> -l <log file>")
    sys.exit(2)

pms = sys.argv[1:]
try:
   opts, args = getopt.getopt(pms,"i:o:l:")
except getopt.GetoptError:
   print("Usage: python ref_links.py -i <link file> -o <link xls file> -l <log file>")
   sys.exit(2)
for opt, arg in opts:
   if opt == "-i":
      link_file = arg
   elif opt == "-o":
      xls_file = arg
   elif opt == "-l":
      log_file = arg

log = open(log_file, "w")
print(datetime.datetime.now(), file=log)

book = xlsxwriter.Workbook(xls_file)
sh = book.add_worksheet("Link Data")

bold = book.add_format({'bold': 1})

sh.write(0, 0, 'Record number', bold)
sh.write(0, 1, 'Source DOI', bold)
sh.write(0, 2, 'Source Accession number', bold)
sh.write(0, 3, 'Destination DOI', bold)
sh.write(0, 4, 'Destination Accession number', bold)

def update_excel(row, record):
    for col, each in enumerate(record):
        sh.write(row, col, each)

record_num = 0
for line in file(link_file, "r"):
    field1 = line.split('|')[0]
    field2 = line.split('|')[1]
    field3 = line.split('|')[2]
    field4 = line.split('|')[3]
    field5 = line.split('|')[4].strip()
    
    record_num+=1
    record = [field1, field2, field3, field4, field5]
    update_excel(record_num, record)
    
book.close()
print(datetime.datetime.now(), file=log)
print("Success", file=log)
log.close()
