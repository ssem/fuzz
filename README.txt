#                               bfg9000
#
# short explination
#
#   1. install python
#   2. python bfg9000.py -g
#
#
#
#
# long explanation
#
#
#   This script grabs random words for a dictionary and preforms a google
#   search on them. Then it takes the first ten results google gives it
#   and parses them for files located on the page. If the file type matches
#   anything found in self.fileTypes located in lib/findFiles.py it will
#   download them. It then adds that downloaded file to the collects directory
#   in the appropriate folder.
#
#   Examples:
#       python bfg9000.py -h
#       python bfg9000.py --help
#       python bfg9000.py default
#       python bfg9000.py < path to dictionary >
#
#   when bfg9000.py runs it creates tmp files. All these tmp files should be
#   automaticaly removed unless something goes wrong
#
#       "tmpFindFiles" this file is a list of all the urls to the files it is
#                      going to download. The schema is type:url.
#
#       "tmpCollects1" this directory is all the downloaded files it found for
#                      the current run.
#
#       "tmpCollects2" this directory is a copy of your collects directory
#
#       "bkCollects"   this is a copy of collects just incase something goes
#                      bad
#

