#!/usr/bin/env python
import sys
from urllib2 import *
import os
from decimal import *

class DownloadFiles:
    def __init__(self):
        self.proxy = None

    def __call__(self, inputFile, outDirect):
        count = 0
        for line in open(inputFile, 'r'):
            fileType = line[:line.find(': ')]
            url = line[line.find(': ') + 2:]
            data = self.getResponse(url)
            if len(data) > 0:
                filename = '%s.%s' % (str(count), fileType)
                path = os.path.join(outDirect, fileType)
                count += 1
                try:os.makedirs(path)
                except: pass
                f = open(os.path.join(path, filename), 'w+')
                f.write(data)
                f.close()
                message = 'Downloading Files: %s' % count
                sys.stdout.write(message)
                sys.stdout.flush()
                sys.stdout.write('\b' * len(message))

    def getResponse(self, url):
        try:
            opener = build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            response = opener.open(str(url))
            for line in response.info():
                if 'Content-Length' in line:
                    if int(line.split(': ')[1]) > 1000000:
                        return ''
            return response.read()
        except: return ''


if __name__=='__main__':
    try:
        test = DownloadFiles()
        test(sys.argv[1], sys.argv[2])
    except IndexError:
        print '\n\tUsage: downloadFile    < Input File >    < Output Directory>\n'

