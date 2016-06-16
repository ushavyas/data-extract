#######################################################
#                                                     #
# Name        : extract_xls.py                        #
# Date        : 06/13/2016                            #
# Description : Program to convert data files into    #
#               excel sheets                          #
# Input File  : data.txt                              #
# Output File : output.xls                            #
# Author      : Usha Boddeda                          #
#                                                     #
#######################################################

from __future__ import print_function
import urllib
import urllib2
import xlsxwriter
from lxml import html
from bs4 import BeautifulSoup
from functions import getValue

xls_file = "/home/usha/python/log/output.xls"

book = xlsxwriter.Workbook(xls_file)
sh = book.add_worksheet("WOS Data")
bold = book.add_format({'bold': 1})

sh.write(0, 0, 'Article Name', bold)
sh.write(0, 1, 'Authors', bold)
sh.write(0, 2, 'Authors Full Names', bold)
sh.write(0, 3, 'Reprint author', bold)
sh.write(0, 4, 'Reprint author address', bold)
sh.write(0, 5, 'Author Org Name(s) 1', bold)
sh.write(0, 6, 'Author Org Name(s) 2', bold)
sh.write(0, 7, 'Author E-mail(s)', bold)
sh.write(0, 8, 'Volume', bold)
sh.write(0, 9, 'Issue', bold)
sh.write(0, 10, 'Pages', bold)
sh.write(0, 11, 'DOI', bold)
sh.write(0, 12, 'Published Date', bold)
sh.write(0, 13, 'Abstract', bold)
sh.write(0, 14, 'Keywords', bold)
sh.write(0, 15, 'Publisher', bold)
sh.write(0, 16, 'Research Domain', bold)
sh.write(0, 17, 'WOS Category', bold)
sh.write(0, 18, 'Document Type', bold)
sh.write(0, 19, 'Language', bold)
sh.write(0, 20, 'Accession Number', bold)
sh.write(0, 21, 'ISSN', bold)
sh.write(0, 22, 'eISSN', bold)
sh.write(0, 23, 'IDS Number', bold)
sh.write(0, 24, 'Number of Cited References', bold)
sh.write(0, 25, 'Number of Citing References', bold)

def update_excel(row, record):
    for col, each in enumerate(record):
        sh.write(row, col, each)

in_file = "/home/usha/python/log/data_n.txt"
record_num = 0
for line in file(in_file, "r"):
    field1 = line.split('|')[0]
    field2 = line.split('|')[1]
    field3 = line.split('|')[2]
    field4 = line.split('|')[3]
    field5 = line.split('|')[4]
    field6 = line.split('|')[5]
    field7 = line.split('|')[6]
    field8 = line.split('|')[7]
    field9 = line.split('|')[8]
    field10 = line.split('|')[9]
    field11 = line.split('|')[10]
    field12 = line.split('|')[11]
    field13 = line.split('|')[12]
    field14 = line.split('|')[13]
    field15 = line.split('|')[14]
    field16 = line.split('|')[15]
    field17 = line.split('|')[16]
    field18 = line.split('|')[17]
    field19 = line.split('|')[18]
    field20 = line.split('|')[19]
    field21 = line.split('|')[20]
    field22 = line.split('|')[21]
    field23 = line.split('|')[22]
    field24 = line.split('|')[23]
    field25 = line.split('|')[24]
    field26 = line.split('|')[25].strip()
    
    record_num+=1
    record = [field1, field2, field3, field4, field5, field6, field7, field8, field9, field10, field11, field12, field13, field14, field15, field16, field17, field18, field19, field20, field21, field22, field23, field24, field25, field26]
    update_excel(record_num, record)
    
book.close()
