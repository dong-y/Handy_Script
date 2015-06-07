import csv
from bs4 import BeautifulSoup
import pprint
import mechanize
import re
import os
from urllib2 import HTTPError
import pprint
import xlwt

browser = mechanize.Browser()
# browser.set_handle_robots(False)
# browser.set_handle_equiv(False) 
browser.addheaders = [('User-Agent', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36"), ('Accept', '*/*')]

what_to_write_in_file_list = []
with open('IP_List_CSV.csv', 'rU') as csvfile:
	IP = csv.reader(csvfile, dialect=csv.excel_tab)
	count = 1
	for row in IP:
		pprint.pprint(count)
		count += 1
		# print ' '.join(row)
		url = "http://whois.domaintools.com"
		url = "http://whois.domaintools.com/" + row[0]
		# browser.addheaders = [('User-Agent', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36"), ('Accept', '*/*')]
		# browser.addheaders = [('user-agent', '   Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'),
# ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
		print url

		response = browser.open(url)

		response = response.read()
		# pprint.pprint(response)
		soup = BeautifulSoup(response)
		raw_tag = soup.findAll("div", { "class" : "raw" })
		pprint.pprint(raw_tag)
		try:
			input_lines = raw_tag.string.split('\n')
		except AttributeError:
			what_to_write_in_file_list.append([row[0], '', ''])
			continue
		# pprint.pprint(input_lines)
		lst = []
		lst.append(row[0])
		for line in input_lines:
			key_value_pair_as_list = line.split(":")
			if str(key_value_pair_as_list[0]) == 'NetRange' or 'inetnum':
				pprint.pprint('NetRange: ' + key_value_pair_as_list[1])
				lst.append(key_value_pair_as_list[1])		
			if str(key_value_pair_as_list[0]) == 'OrgName' or 'descr':
				pprint.pprint('OrgName: ' + key_value_pair_as_list[1])
				lst.append(key_value_pair_as_list[1])
		what_to_write_in_file_list.append(lst)
	csvfile.close()

workbook = xlwt.Workbook() 
sheet = workbook.add_sheet("Sheet1")

for i in range(0, len(what_to_write_in_file_list)):
	for j in range(len(what_to_write_in_file_list[i])):
		sheet.write(i, j, what_to_write_in_file_list[i][j].strip())

workbook.save("output.xls") 

# with open('output.csv', 'wb') as csvfile:
# 	spamwriter = csv.writer(csvfile, dialect=csv.excel_tab)
# 	for item in what_to_write_in_file_list:
# 		print item
# 		spamwriter.writerow(item)
# 	csvfile.close()

