import re
import sys
from collections import Counter

import mechanize 
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner
import nltk
# Uncomment below if nltk hasn't been downloaded
# nltk.download()
from itertools import chain


from nltk.corpus import stopwords
from urllib2 import urlopen, Request


def getArticles(keyword):
	cleaner = Cleaner()
	cleaner.javascript = True
	cleaner.style = True

	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders=[('User-agent','chrome')]
	# Change num=#, to whatever the number of pages you want to crawl.
	term = keyword.replace(" ", "+")
	query = "http://www.google.ca/search?&tbm=nws&num=10&q=" + term 
	htmltext = br.open(query).read()
	#print htmltext

	soup = BeautifulSoup(htmltext)

	search = soup.findAll('div', attrs={'id': 'search'})
	#print search[0]
	searchtext= str(search[0])
	soup1=BeautifulSoup(searchtext)
	list_items=soup1.findAll('li')

	regex = "q=.*?&amp"	
	pattern = re.compile(regex)
	results_array = []
	for li in list_items:
		soup2 = BeautifulSoup(str(li))
		links = soup2.findAll('a')
		source_link = links[0]
		#print source_link
		source_url = re.findall(pattern, str(source_link))
		if len(source_url) > 0:
				results_array.append(str(source_url[0].replace("q=", "").replace("&amp", "")))
	return results_array


def parser(results_array):
	all_text = []
	hdr = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'})
	for url in results_array:
		text_data = urlopen(Request(url, headers= hdr)).read().decode('unicode_escape').encode('ascii','ignore')
		for paragraph in re.findall(r'<p>(.*?)</p>', text_data):
			all_text.append(re.sub(r'<([^>]+)>', '', paragraph))
	return all_text

def main():
	totalCounts = []
	keyword = raw_input("Enter what you would like to search: ")
	print "This will take a moment...."
	counts = Counter([word.lower() for list_of_words in [paragraph.split() for paragraph in parser(getArticles(keyword))] for word in list_of_words 
		if word not in stopwords.words('english')])
	print counts

if __name__ == '__main__':
	main()