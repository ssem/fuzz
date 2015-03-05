#!/usr/bin/env python
import os
import sys
import argparse
import requests

class Http:
    def __init__(self, ip, port, firmware=None, verbose=None):
        self.ip = ip
        self.port = port
        self.firmware = firmware
        self.verbose = verbose

    def find_unauth_urls(self):
        if self.firmware is not None:
            paths = set(self._find_all_paths())
        else:
            try:
                paths = set(open('lib/default_paths', 'r'))
            except:
                paths = set(open('default_paths', 'r'))
        valid = {}
        for path in paths:
            print path
            url = 'http://%s:%s%s' % (self.ip, self.port, path)
            if callable(self.verbose):
                self.verbose('Request %s' % url)
            try:
                http = requests.get(url)
                valid[http.content] = url
            except:pass
        for url in valid:
            yield valid[url]

    def _find_all_paths(self):
        web = {}
        for dpath, dnames, fnames in os.walk(self.firmware):
            for f in fnames:
                # filter in
                if f.endswith('.htm') or f.endswith('.html') \
                or f.endswith('.asp') or f.endswith('js') \
                or f.endswith('.ha') or f.endswith('.css') \
                or f.startswith('index.'):
                    web[dpath] = ''
        for w in web:
            for dpath, dnames, fnames in os.walk(w):
                for f in fnames:
                    # filter out
                    if f.endswith('.jpg') or f.endswith('.png') \
                    or f.endswith('.jpeg') or f.endswith('.gif'):
                        continue
                    yield '/%s' % f
                    yield '/%s' % os.path.join(os.path.basename(w), f)
        yield '/'

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('ip', help='target ip address')
    parse.add_argument('port', help='target port number')
    parse.add_argument('-f', metavar=('file'),
        help='path to extracted firmware of target')
    parse.add_argument('-o', metavar=('file'),
        help='output file')
    args = parse.parse_args()
    http = Http(args.ip, args.port, args.f)
    if args.o:
        f = open(args.o, 'w+')
    else:
        f = sys.stdout
    for path in http.find_unauth_urls():
        f.write('%s\n' % path)

