#!/usr/bin/env python
import sys
import time
import subprocess

#
# Control script to process tweets.
# 1. download twitter streams into a file using twitterstream.py into tweets_output.json
# 2. process tweets_output.json with happiest_states.json
#

if __name__ == "__main__":
    try:
        # outputs tweets to file
        f = open('tweets_output.json','w')
        process = subprocess.Popen(["./twitterstream.py"], stdout=f, stderr=subprocess.PIPE)
        
        print 'Gathering tweets for 10 minutes'
        
        time.sleep(600)
        process.kill()
        
        out, err = process.communicate()
        errcode = process.returncode
        print 'return code', errcode
        
        # process tweets to find happiest states
        statesProcess = subprocess.Popen(["./happiest_state.py","AFINN-111.txt","tweets_output.json"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = statesProcess.communicate()
        errcode = statesProcess.returncode
        print out
        print 'return code', errcode
        
    
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e