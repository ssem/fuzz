#!/usr/bin/env python
import os
import sys
import time
import argparse
import multiprocessing 
from subprocess import Popen, PIPE

def worker((cmd, tyme)):
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    time.sleep(int(tyme))
    if process.poll() > 0:
        print cmd, tyme
    try:
        process.kill()
    except: pass
    try:
        process.terminate()
    except: pass

class Fuzz:
    def __init__(self):
        pass

    def start(self, cmd, tyme, limit, in_files=None): 
        pool = multiprocessing.Pool(int(limit))
        jobs = self._create_cmds(cmd, tyme, in_files)
        pool.map(worker, jobs) 

    def _create_cmds(self, cmd, tyme, in_files):
        cmds = ()
        if in_files:
            in_files = os.path.expanduser(in_files)
            for f in os.listdir(in_files):
                file_name = os.path.join(in_files, f)
                cmds += ([cmd.replace('#if', file_name).split(' '),tyme],)
        return cmds

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('cmd', help='cmd to run')
    parse.add_argument('-if', dest='in_files',
        help='dir of files fro input')
    parse.add_argument('-t', dest='time', default=5,
        help='run process for T sec (DEFAULT: 5)')
    parse.add_argument('-n', dest='limit', default=5,
        help='limit to N processes (DEFAULT: 5)')
    args = parse.parse_args()
    fuzz = Fuzz()
    fuzz.start(args.cmd, args.time, args.limit, args.in_files)
