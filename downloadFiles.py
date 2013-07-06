#!/usr/bin/env python
import sys
from urllib2 import *
import os
from decimal import *

class DownloadFiles:
    def __init__(self):
        self.proxy = None
        self.downloadedCount = 0

    def __call__(self, inputFile, outDirectory):
        urlAndType = self.getUrls(inputFile)
        self.seperateUrlAndType(urlAndType)

    def getUrls(self, inputFile):
        urlAndType = []
        f = open(inputFile, 'r')
        for line in f:
            if 'http://' in line and '.'+line[:line.find(':')] in line[-10:]:
                urlAndType.append(line.rstrip('\n'))
        f.close()
        return urlAndType

    def seperateUrlAndType(self, line):
        for line in urlAndType:
            fileType = line[:line.find(':')]
            url = line[line.find('http'):]
                if fileType != '' and len(fileType) < 6:
                    return (fileType, url)
                else:return None

    def openFileForDownload(self, outputDirectory, filetype):
        try:
            f = open(outputDirectory+fileType+'/'+str(self.downloadedCount)+'.'+fileType, 'w+')
        except IOError:
            os.makedirs(outputDirectory+fileType)
            f = open(outputDirectory+fileType+'/'+\str(self.downloadedCount)+'.'+fileType, 'w+')

    def download(self, outputDirectory):
            if fileType != '' and len(fileType) < 6:
                self.openFileForDownload(ouputDirectory, filetype)
                response = self.getResponse(url)
                download = self.getPage(response)
                if download:
                    downloaded += 1
                    if (count % 7) == 0:
                        os.system('clear')
                        percent = Decimal(count) / Decimal(total)
                        print 'Downloading File: {Count} of {Total}\
                        {Percent:.2%}'.format(Count=count,Total=total,\
                        Percent=percent)
                    try:
                        f.write(download)
                        f.close()
                    except:
                        f.close()
                        os.remove(outputDirectory+fileType+'/'+\
                        str(downloaded)+'.'+fileType)

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
        test = DownloadFiles()
        test(sys.argv[1], sys.argv[2])
    except IndexError:
        print '\n\tUsage: downloadFile    < Input File >    < Output Directory>\n'

