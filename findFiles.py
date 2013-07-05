#!/usr/bin/env python
import os
import sys
from urllib2 import *
from lib.google import *
import random

class GetFiles:
    def __init__(self, dictionary, output, port=80, proxy=False):
        self.port = port
        self.proxy = proxy
        self.output = open(output, 'w+')
        self.inputFile = open(dictionary, 'r')

    def run(self):
        count = 0
        totalItemsFound = 0
        urls, total = self.getUrlsAndTotalCount()
        for url in urls:
            count += 1
            os.system('clear')
            print 'Parsing Urls: '+str(count)+' of '+str(total)+'      #'+str(totalItemsFound)
            response = self.getResponse(url)
            if response:
                page = self.getPage(response)
                domain = self.getUrl(response)
                totalItemsFound += self.filterPage(page, domain)
        self.output.close()

    def getUrlsAndTotalCount(self):
        words = []
        urls = []
        totalWords = 0
        totalUrls = 0
        print 'Loading Dictionary file'
        for item in self.inputFile:
            totalWords += 1
            words.append(item)
        self.inputFile.close()
        for numberOfSearchesToPreform in xrange(100):
            searchString = ''
            for numberOfWordsForSearching in xrange(random.randrange(1,2)):
                searchString += words[random.randrange(1,totalWords)].rstrip('\n')+' '
            try:
                googleResults = google.search(str(searchString),stop=1)
                for googleResult in googleResults:
                    totalUrls += 1
                    urls.append(googleResult)
            except: pass
            os.system('clear')
            print 'Acquiring Urls      # '+str(totalUrls)
        return (urls, totalUrls)

    def filterPage(self, page, domain):
        count = 0
        fileTypes = ['.css','.pdf','.webarchive','.webbookmark','.webhistory','.webloc',\
        '.download','.safariextz','.gif','.htm','.js','.jpg','.jpeg','.jp2','.txt','.text',\
        '.png','.tif','.url','.ico','.xhtml','.xht','.xml','.xbl','.xbl','.svg']
        try:
            items = page.split(' ')
        except AttributeError: pass
        for item in items:
            for fileType in fileTypes:
                if fileType in item.lower():
                    if '"' in item.lower():
                        item = item[item.find('"')+1:]
                        item = item[:item.find('"')]
                    elif "'" in item.lower():
                        item = item[item.find("'")+1:]
                        item = item[:item.find("'")]
                    if len(item) > 4:
                        if item.startswith('http:'):
                            foundItem = fileType.lstrip('.')+': '+item
                        else:
                            foundItem = fileType.lstrip('.')+': '+domain+item
                        count += 1
                        self.output.write(foundItem+'\n')
        return count

    def getResponse(self, url):
        try:
            if self.proxy:
                proxy = ProxyHandler({'http': self.proxy})
                opener = build_opener(proxy)
            else:
                opener = build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            return opener.open(str(url))
        except HTTPError as e:
            return None
        except URLError as e:
            return None

    def getHeader(self, response):
        return str(response.info())

    def getUrl(self, response):
        return str(response.geturl())

    def getPage(self, response):
        try:
            response = str(response.read())
        except: pass
        return response

if __name__=='__main__':
    try:
        test = GetFiles(sys.argv[1], sys.argv[2])
        test.run()
    except IndexError:
        print '\n\tUsage: findFiles.py      < path to dictionary>    < outfile >\n'


