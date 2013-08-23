#!/usr/bin/env python
import os
import sys
from urllib2 import *
import google
import random

class FindFiles:
    def __init__(self, port=80, proxy=False):
        self.port = port
        self.proxy = proxy
        self.fileTypes = ['.css','.pdf','.webarchive','.webbookmark','.webhistory','.webloc',\
        '.download','.safariextz','.gif','.htm','.js','.jpg','.jpeg','.jp2','.txt','.text',\
        '.png','.tif','.url','.ico','.xhtml','.xht','.xml','.xbl','.xbl','.svg']

    def __call__(self, dictionary, output, rounds=1):
        totalFoundItems = 0
        os.system('clear')
        print '[ Loading Dictionary ]'
        words = self.getRandomWords(dictionary)
        for x in xrange(rounds):
            print '\n[ Round %s of rounds %s]' % (str(x+1), str(rounds))
            searchString = self.makeSearchString(words)
            print '[ Getting Search Results For %s ]' % searchString
            urls = self.getUrls(searchString)
            print '    - [ Found %s Urls ]' % len(urls)
            pages = self.getPage(urls)
            foundItems = self.filterPages(pages)
            print '    - [ Found %s Items ]' % len(foundItems)
            totalFoundItems += len(foundItems)
            print '    - [ Total %s ]' % totalFoundItems
            self.saveToFile(foundItems, output)

    def saveToFile(self, foundItems, output):
        try:
            f = open(output, 'a')
            for item in foundItems:
                f.write(item+'\n')
            f.close()
        except: pass

    def getPage(self, urls):
        pages = {}
        for url in urls:
            response = self.getResponse(url)
            domain = self.getUrlFromResponse(response)
            if response:
                pages[self.getPageFromResponse(response)] = domain
        return pages

    def getRandomWords(self, dictionary):
        words = []
        f = open(dictionary, 'r')
        for item in f:
            words.append(item)
        f.close()
        if len(words) < 1:
            print '\n\tUsage: findFiles.py      < path to dictionary>    < outfile >\n'
            exit()
        return words

    def makeSearchString(self, words):
        searchString = ''
        for x in xrange(random.randrange(1,3)):
            searchString += words[random.randrange(1,len(words))].rstrip('\n')+' '
        return searchString.rstrip(' ')

    def getUrls(self, searchString):
        try:
            urls = []
            googleResults = google.search(str(searchString),stop=1)
            for item in googleResults:
                urls.append(item)
            return urls
        except:return None

    def filterPages(self, pages):
        foundItems = []
        for page in pages:
            try:
                items = page.split(' ')
                domain = pages[page]
                for item in items:
                    for fileType in self.fileTypes:
                        foundItem = self.filterPage(fileType, item, domain)
                        if foundItem:
                            foundItems.append(foundItem)
            except AttributeError: pass
        return foundItems

    def filterPage(self, fileType, item, domain):
        foundItem = None
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
        return foundItem

    def getResponse(self, url):
        try:
            if self.proxy:
                proxy = ProxyHandler({'http': self.proxy})
                opener = build_opener(proxy)
            else:opener = build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            return opener.open(str(url))
        except Exception:return None
    def getHeaderFromResponse(self, response):
        try:return str(response.info())
        except: return None
    def getUrlFromResponse(self, response):
        try:return str(response.geturl())
        except: return None
    def getPageFromResponse(self, response):
        try:return str(response.read())
        except: return None

if __name__=='__main__':
    try:
        test = FindFiles()
        test(sys.argv[1], sys.argv[2])
    except IndexError:
        print '\n\tUsage: findFiles.py      < path to dictionary>    < outfile >\n'


