#!/usr/bin/env python
import sys
from urllib2 import *
import os
from decimal import *

class DownloadFiles:
    def __init__(self):
        self.proxy = None

    def __call__(self, inputFile, outDirect):
        lines = self.getLines(inputFile)
        urlsAndTypes = self.getUrlsAndTypes(lines)
        for index, url in enumerate(urlsAndTypes):
            outputFile=self.openFile(outDirect,urlsAndTypes[url],index)
            if not self.download(url, outputFile):
                self.removeBadFile(outDirect,urlsAndTypes[url],index)
            self.printStatus(index, len(urlsAndTypes))

    def printStatus(self, index, total):
        percent = Decimal(index) / Decimal(total)
        message = 'Downloading Files: {Percent:.2%}'.format(
            Count=index,Total=total,Percent=percent)
        sys.stdout.write(message)
        sys.stdout.flush()
        sys.stdout.write('\b' * len(message))

    def getLines(self, inputFile):
        lines = []
        f = open(inputFile, 'r')
        for line in f:
            if 'http://' in line and '.'+line[:line.find(':')] in line[-10:]:
                lines.append(line.rstrip('\n'))
        f.close()
        return lines

    def getUrlsAndTypes(self, lines):
        urlsAndTypes = {}
        for line in lines:
            fileType = line[:line.find(':')]
            url = line[line.find('http'):]
            if fileType != '' and len(fileType) < 6:
                urlsAndTypes[url]=fileType
        return urlsAndTypes

    def openFile(self, outDirectory, fileType, count):
        if not outDirectory.endswith('/'):
            outDirectory = outDirectory+'/'
        try:
            f = open(outDirectory+fileType+'/'+str(count)+'.'+fileType, 'w+')
        except IOError:
            os.makedirs(outDirectory+fileType)
            f = open(outDirectory+fileType+'/'+str(count)+'.'+fileType, 'w+')
        return f

    def download(self, url, outputFile):
        response = self.getResponse(url)
        if self.filterBasedOnSize(response):
            download = self.getPage(response)
            if download:
                try:
                    outputFile.write(download)
                    outputFile.close()
                    return True
                except:pass
        outputFile.close()
        return False

    def filterBasedOnSize(self, response):
        header = self.getHeader(response)
        if header:
            for line in header.split('\n'):
                if 'Content-Length' in line:
                    length = line.split(': ')[1]
                    if int(length) < 1000000: return True
        return False

    def removeBadFile(self, outDirectory, fileType, count):
        try:
            os.remove(outDirectory+fileType+'/'+str(count)+'.'+fileType)
        except:
            try:
                os.remove(outDirectory+'/'+fileType+'/'+str(count)+\
                '.'+fileType)
            except:pass
    
    def getResponse(self, url):
        try:
            if self.proxy:
                proxy = ProxyHandler({'http': self.proxy})
                opener = build_opener(proxy)
            else:
                opener = build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            return opener.open(str(url))
        except: return None
    
    def getHeader(self, response):
        try:
            return str(response.info())
        except: return None
    
    def getUrl(self, response):
        try:
            return str(response.geturl())
        except: return None
    
    def getPage(self, response):
        try:
            return str(response.read())
        except: return None


if __name__=='__main__':
    try:
        test = DownloadFiles()
        test(sys.argv[1], sys.argv[2])
    except IndexError:
        print '\n\tUsage: downloadFile    < Input File >    < Output Directory>\n'

