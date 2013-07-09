import urllib2
import random
import re
from urllib import urlopen
from bs4 import BeautifulSoup
import subprocess
import sys



voices =['Agnes','Kathy','Prince','Vicki','Victoria','Bruce','Fred','Junior','ralph','whisper']

hdrs = { 'User-Agent': "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11" }

shouldTalk = False;

try:
    shouldTalk = sys.argv[1].lower() =='talk' or sys.argv[1].lower() == 'yes' or sys.argv[1].lower()=='on' or sys.argv[1].lower()=='lemmehearyourvoice'
except:
    pass

link0 = ('http://en.wikipedia.org/wiki/Main_Page');


random.seed()


def readPage(page):
    
    #not sure why we need this, but I guess some wikipedia asks for it
    
    req = urllib2.Request(page , headers = {'User-Agent': "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"})
    
    #opens new page
    
    fd = urllib2.urlopen(req)
    
    #returns entire html
    
    soup = BeautifulSoup(fd)
    
    #this is the key line: all links are inside <a></a> so lets get every <a></a> in the html
    
    linkList = soup.find_all('a')
    while len(linkList) > 0:
        rand = random.randint(0,len(linkList)-1)
        
        #pick a random link
        
        link = linkList[rand]
        
        #get the href (link) from each component
        
        newComponent = str(link.get('href'));
        
        #clean out links that are too frequent or lead you to another website
        
        if (":" in newComponent) or ("#" in newComponent) or ("?" in newComponent) or ("&" in newComponent) or ("Main_Page" in newComponent):
            linkList.pop(rand);
            continue
        newpage='http://en.wikipedia.org'+str(link.get('href'));
    
        #the link might be invalid so we sould check if it is valid before adding it to the list
    
        try:
            req = urllib2.Request(newpage , headers = {'User-Agent': "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"})
            fd = urllib2.urlopen(req)
            soup = BeautifulSoup(fd)
            return newpage;
        except:
            linkList.pop(rand)

#below is the first code to execute
#First create the Request object, using the headers argument to change the UserAgent.

req = urllib2.Request(link0 , headers = hdrs)

#use the Request Object to fetch the page.

fd = urllib2.urlopen(req)
soup = BeautifulSoup(fd)
linkList = soup.find_all('a')
currentLink = link0;
while True:
    
    #this continues indefinitely
    
    currentLink = readPage(currentLink)
    name = currentLink.replace('http://en.wikipedia.org/wiki/', '')
    name = re.sub('[.!,;_%]', ' ', name)
    print name
    if shouldTalk:
    	try:
    		subprocess.call(['/usr/bin/say','-v'+voices[random.randint(0,9)],'-r0.3',name])
    	except:
		pass

    
    
    
        
         
            
            
            
        
