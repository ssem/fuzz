#!/usr/bin/env python
import os
import re
import sys
from urllib2 import *
import google
import random

class FindFiles:
    def __init__(self):
        self.fileTypes = ['.css','.pdf','.webarchive','.webbookmark',
            '.webhistory','.webloc','.download','.safariextz','.gif',
            '.htm','.js','.jpg','.jpeg','.jp2','.txt','.text','.png',
            '.tif','.url','.ico','.xhtml','.xht','.xml','.xbl','.xbl','.svg']
        self.regex = '(https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?)'

    def __call__(self, dictionary, output, rounds=1):
        print '[ Loading Dictionary ]'
        f = open(dictionary, 'r')
        words = list(f)
        f.close()
        f = open(output, 'w+')
        for x in xrange(int(rounds)):
            print '[ Round %s of %s]' % (str(x+1), str(rounds))
            searchString = random.choice(words).rstrip('\n')
            print '    - [ Searching For %s ]' % searchString
            for url in google.search(searchString, stop=1):
                matches = re.findall(self.regex, self.getResponse(url))
                print '    - [ %s  %s Matches ]' % (url, len(matches))
                for match in matches:
                    for fileType in self.fileTypes:
                        if match[0].endswith(fileType):
                            f.write('%s: %s\n' % (fileType.lstrip('.'), match[0]))
        f.close()

    def getResponse(self, url):
        try:
            opener = build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            response = opener.open(str(url))
            return response.read()
        except Exception:return ''

if __name__=='__main__':
    try:
        test = FindFiles()
        test(sys.argv[1], sys.argv[2])
    except IndexError:
        print '\n\tUsage: findFiles.py      < path to dictionary>    < outfile >\n'


