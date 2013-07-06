#!/usr/bin/env python
import sys
import os

class combineCollects:
    def __init__(self):
        pass

    def __call__(self, directories, output):
        self.makeOutputFile(output)
        filePaths = self.getFilePaths(directories)
        self.renameFiles(filePaths, output)
        self.removeOldDirectories(directories)

    def removeOldDirectories(self, directories):
        for directory in directories:
            for root, direct, files in os.walk(directory):
                for d in direct:
                    os.rmdir(root+d)
                os.rmdir(root)

    def renameFiles(self, filePaths, output):
        for index, filePath in enumerate(filePaths):
            d = filePath.split('/')[-2]
            try:
                os.rename(filePath, '%s/%s/%s.%s'% (output,d,index,d))
            except OSError as e:
                os.mkdir(output+'/'+d)
                os.rename(filePath, '%s/%s/%s.%s'% (output,d,index,d))

    def getFilePaths(self, directories):
        filePaths = []
        for directory in directories:
            for root, direct, files in os.walk(directory):
                for f in files:
                    filePaths.append(root+'/'+f)
        return filePaths

    def makeOutputFile(self, output):
        try:
            os.makedirs(output)
        except OSError:pass

if __name__=='__main__':
    try:
        test = sys.argv[3]
        combine = combineCollects()
        combine(sys.argv[1:-1], sys.argv[-1])
    except IndexError:
        print '\n\tUsage: combineCollects.py  < collects .. > < output directory>\n'
