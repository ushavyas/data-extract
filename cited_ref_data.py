#######################################################
#                                                     #
# Name        : cited_ref_data.py                     #
# Date        : 06/13/2016                            #
# Description : Program to extract Cited references   #
#               data and corresponding connecting data#
# Input File  : cited_ref_result.txt                  #
# Output File : cited_ref_data.txt, cited_ref_link.txt#
# Author      : Usha Boddeda                          #
#                                                     #
#######################################################

from __future__ import print_function
from functions import extract_data

in_file = "/home/usha/python/log/cited_ref_result_n.txt"
out_file = "/home/usha/python/log/cited_ref_data.txt"
out2_file = "/home/usha/python/log/cited_ref_link.txt"
out = open(out_file, "a")
out2 = open(out2_file, "a")

print("Extracting cited reference data....")
for cnt, line in enumerate(file(in_file, "r")):
    rec_num = line.split('|')[0]
    src_doi = line.split('|')[1]
    src_an = line.split('|')[2]
    field1 = line.split('|')[3]
    url = line.split('|')[4]
    if url.strip() != "No link" and url.strip() != "None of the Citing Articles are in your subscription":
        try:
            print("Extract record")
            record = extract_data(url)
            print(record)
            dst_doi = record.split('|')[11]
            dst_an = record.split('|')[20]
            link_rec = "|".join([rec_num, src_doi, src_an, dst_doi, dst_an])
        except IOError:
            print("Test")
            record = field1 + "|||||||||||||||||||||||||"
            link_rec = "|".join([rec_num, src_doi, src_an, "", ""])
    else:
        record = field1 + "|No link for data||||||||||||||||||||||||"
        link_rec = "|".join([rec_num, src_doi, src_an, "", ""])
    print("%s%s" % (field1, record), file=out)
    print(link_rec, file=out2)

out.close()
out2.close()
cnt=cnt+1
print("Extracted %s cited reference records" % (cnt))
