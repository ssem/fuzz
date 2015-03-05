#!/usr/bin/env python
import re
import sys
import argparse
import requests
import findUrls

class FindFiles:
    def __init__(self, fileTypes):
        self.fileTypes = fileTypes
        self.regex = '(https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?)'

    def _find_urls(self, dictionary):
        for word in open(dictionary, 'r'):
            for url in findUrls.search(word.rstrip('\n'), stop=1):
                for match in re.findall(self.regex, requests.get(url,verify=False).content):
                    yield url

    def scrape(self, dictionary):
        for url in self._find_urls(dictionary):
            for fType in self.fileTypes:
                if url.endswith(fType):
                    yield url

if __name__=='__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--all', help="add all files", action="store_true")
    parse.add_argument('--css', help="add css files", action="store_true")
    parse.add_argument('--pdf', help="add pdf files", action="store_true")
    parse.add_argument('--gif', help="add gif files", action="store_true")
    parse.add_argument('--js', help="add js files", action="store_true")
    parse.add_argument('--jpg', help="add jpg files", action="store_true")
    parse.add_argument('--jpeg', help="add jpeg files", action="store_true")
    parse.add_argument('--txt', help="add text files", action="store_true")
    parse.add_argument('--text', help="add text files", action="store_true")
    parse.add_argument('--png', help="add png files", action="store_true")
    parse.add_argument('--tif', help="add tif files", action="store_true")
    parse.add_argument('--xml', help="add xml files", action="store_true")
    parse.add_argument('--svg', help="add svg files", action="store_true")
    args = parse.parse_args()
    if len(sys.argv) < 2:
        parse.print_help()
        exit()
    fTypes = []
    if args.css:
        fTypes.append('.css')
    if args.pdf:
        fTypes.append('.pdf')
    if args.gif:
        fTypes.append('.gif')
    if args.js:
        fTypes.append('.js')
    if args.jpg:
        fTypes.append('.jpg')
    if args.jpeg:
        fTypes.append('.jpeg')
    if args.text:
        fTypes.append('.text')
    if args.txt:
        fTypes.append('.txt')
    if args.png:
        fTypes.append('.png')
    if args.tif:
        fTypes.append('.tif')
    if args.xml:
        fTypes.append('.xml')
    if args.svg:
        fTypes.append('.svg')
    if args.all:
        fTypes = ['.css','.pdf','.gif','.js','.jpg','.jpeg','.txt',
            '.text','.png','tif','.xml','.svg']
    find = FindFiles(fTypes)
    for url in find.scrape('dict.txt'):
        print url
