import os
import sys
import shutil
from lib.findFiles import FindFiles
from lib.downloadFiles import DownloadFiles
from lib.combineCollects import CombineCollects

class BFG9000:
    def __init__(self):
        self.find = FindFiles()
        self.download = DownloadFiles()
        self.combine = CombineCollects()

    def __call__(self, dictionary = 'lib/dict.txt', output='tmpCollects1'):
        self.find(dictionary, 'tmpFindFiles')
        self.download('tmpFindFiles', output)
        os.system('clear')
        print '[ Creating collects backup ]'
        shutil.copytree('collects', 'bkCollects')
        os.rename('collects','tmpCollects2')
        print '[ Combining collects ]'
        self.combine(['tmpCollects1', 'tmpCollects2'], 'collects')
        print '[ Removing collects backup ]'
        shutil.rmtree('bkCollects')
        print '[ Finished ]'

    def __del__(self):
        try: os.remove('tmpFindFiles')
        except: pass

def _help():
    print '\n\tExample: bfg9000.py   default'
    print '\tExample: bfg9000.py   < dict >\n'
    exit()

if __name__=='__main__':
    bfg9000 = BFG9000()
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h': _help()
        elif sys.argv[1] == '--help': _help()
        elif sys.argv[1] == 'default': bfg9000()
        else: bfg9000(sys.argv[1])
    else: _help()
