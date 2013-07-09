import urllib2
import random
import re
import subprocess
from urllib import urlopen
from bs4 import BeautifulSoup
import csv
import sys


csvWriter = csv.writer(open('../data/whitmanData.txt', 'w', buffering=0));


random.seed()

def constructCorrospondanceList(page):
    req = urllib2.Request(page)
    fd = urllib2.urlopen(req) 
    soup = BeautifulSoup(fd)
    linkList = soup.find(id='bibliography');
    cleanedList = linkList.find_all('a');
    letterLinkList = []
    for letter in cleanedList:
		letterLinkList.append(letter.get('href'))
    return letterLinkList;
    	# for link in cleanedList:
    # 	print link.get('href')
    # 	print link.get_text()

def readLetter(page):

	letterText = ''
	heading = None
	req = urllib2.Request(page)
	fd = urllib2.urlopen(req)
	soup = BeautifulSoup(fd)
	letter = soup.find(id='body')
	try:
		heading = letter.find('h3').get_text()
		letterBody = letter.find_all('div')
		letterText = letterBody[0].get_text();
		print 'type 1'
	except:
		metaData = letter.find(id='metadata')
		metaDatas = metaData.find_all('p')
		heading = metaDatas[0].get_text();
		heading = heading[7:len(heading)]
		heading = heading.replace('[','')
		heading = heading.replace(']','')
		letterBody = letter.find_all('div')
		letterText = letterBody[len(letterBody)-1].get_text();
		print 'type 2'
	page = page.replace(u'\xa0',' ').encode('utf-8')
	heading = heading.replace(u'\xa0',' ').encode('utf-8')
	letterText = letterText.replace(u'\xa0',' ').encode('utf-8')
	row = [page,heading,letterText]
	csvWriter.writerow(row)

	return letterText

def randomLetterRead():
	letterList = constructCorrospondanceList('http://www.whitmanarchive.org/biography/correspondence/index.html')
	while True:
		#try:
			rand = random.randint(0,len(letterList)-1)
			letterToReadLink = letterList[rand][5:len(letterList[rand])]
			textToRead = readLetter('http://www.whitmanarchive.org/'+str(letterToReadLink))
			print textToRead
			#subprocess.call(['/usr/bin/say','-vKathy','-r0.3',textToRead])
			break
		#except:
			print 'failed'
			break
			#continue

def collectData():
	links = constructCorrospondanceList('http://www.whitmanarchive.org/biography/correspondence/index.html')
	counter = 0;
	for link in links:
		
		link = link[5:len(link)]
		link = 'http://www.whitmanarchive.org'+str(link)
		print counter
		counter = counter +1
		try:
			readLetter(link)
		except:
			print 'BAD LINK'



collectData();




	


	

