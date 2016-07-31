#!/usr/bin/env python
'''
Created on July 31, 2016
@author: Houston Harris
'''

import sys
import string
import json
import datetime
from pymongo import MongoClient

def main():
    # track happiness over time
    happinessByDate = {};

    # insert into local mongo
    client = MongoClient('localhost', 27017)
    db = client.twit_data
    happyStates = db.happiest_states
    happiest_times = db.happiest_times

    #record = happyStates.find_one()
    for record in happyStates.find():
        totalScore = 0
        # can we iterate through attrs?
        for attr in record:
            #print attr
            if attr != 'parseDate' and attr != '_id' and attr != 'hashtags':
                state = record[attr]
                if 'score' in state and state['score'] != 'NA':
                    #print attr + ':' + str(state['score'])
                    totalScore += state['score']
        # now we have total for that record
        print 'Total score on ' + str(record['parseDate']) + ' : ' + str(totalScore)
        # lets try and insert into collection
        happiest_times.insert({'parseDate':record['parseDate'], 'score':totalScore})

if __name__ == '__main__':
    main()
