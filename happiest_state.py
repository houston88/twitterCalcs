#!/usr/bin/env python
'''
Created on May 13, 2013
@author: Houston Harris
'''

import sys
import string
import json
import datetime
from pymongo import MongoClient

def main():
    afinnfile = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    afinnfile = open(sys.argv[1])
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        # The file is tab-delimited. "\t" means "tab character"
        term, score  = line.split("\t")
        # Convert the score to an integer.        
        scores[term] = int(score)
        
    # Print every (term, score) pair in the dictionary
    #print scores.items()
    
    # list of states to use
    states = [
        'AL',
        'AK',
        'AS',
        'AZ',
        'AR',
        'CA',
        'CO',
        'CT',
        'DE',
        'DC',
        'FM',
        'FL',
        'GA',
        'GU',
        'HI',
        'ID',
        'IL',
        'IN',
        'IA',
        'KS',
        'KY',
        'LA',
        'ME',
        'MH',
        'MD',
        'MA',
        'MI',
        'MN',
        'MS',
        'MO',
        'MT',
        'NE',
        'NV',
        'NH',
        'NJ',
        'NM',
        'NY',
        'NC',
        'ND',
        'MP',
        'OH',
        'OK',
        'OR',
        'PW',
        'PA',
        'PR',
        'RI',
        'SC',
        'SD',
        'TN',
        'TX',
        'UT',
        'VT',
        'VI',
        'VA',
        'WA',
        'WV',
        'WI',
        'WY'
    ]
    
    # keep track of hapiness by state
    state_hapiness = {}
    
    # lets try and load json output
    tweet_file = open(sys.argv[2])
    for line in tweet_file:
        lineData = {}
        try:
            lineData = json.loads(line)
        except:
            lineData = {}
            #print 'Hmmm... encountered an error, oh well...'
        
        #print lineData
        
        # limit to tweets that have a place
        
        # To limit to US
        # place['country_code'] = "US"
        # place['coordinates'] = [ [2.2241006,48.8155414], [2.4699099,48.8155414], [2.4699099,48.9021461], [2.2241006,48.9021461] ] ]
        
        # Use coordinates to calc state
        # coordinates['coordinates'] = [-75.14310264,40.05701649]
        
        # unreliable, but could try:
        # user['location'] = "San Francisco, CA"
        
        if 'place' in lineData and lineData['place']:
            # we have a place, lets print the place data
            placeData = lineData['place']
            
            if (placeData['country_code'] and placeData['country_code']=='US'):
                #print 'Place is in the US! Continue...'
                #print placeData
                
                state = 'UNKN'
                
                # lets just use the place_type = city, seems to be common enough
                if 'place_type' in placeData:
                    
                    placeTypeStr = placeData['place_type'].encode('utf-8')
                    placeFillNameStr = placeData['full_name'].encode('utf-8')
                    
                    if (placeTypeStr == 'city' and (placeFillNameStr.find(",") != -1)):
                        city, state  = placeFillNameStr.split(",")
                        state = state.strip()
                    elif placeTypeStr == 'state':
                        state = placeData['full_name']
                
                #print 'We have a state: ' + state
                
                if state != 'UNKN':
                    tweetScore = 0
                    if 'text' in lineData:
                        line_txt = lineData['text']
                        str_txt = line_txt.encode('utf-8')
                        
                        # remove common punctuation
                        exclude = set(string.punctuation)
                        line_txt_no_punc = ''.join(ch for ch in str_txt if ch not in exclude)
                        
                        # see if word in afin list
                        words = line_txt_no_punc.split();
                        for word in words:
                            # lowercase
                            wordLower = word.lower()
                            
                            if wordLower in scores:
                                tweetScore += scores[wordLower]
                                #print 'Word: ' + wordLower + ' Sentiment score: ' + str(scores[word])
                     
                    # we have a score for tweet           
                    #print float(tweetScore)
                    
                    
                    # add score to total state score
                    if state in state_hapiness:
                        curHappiness = state_hapiness[state]
                        curHappiness += tweetScore
                        state_hapiness[state] = curHappiness
                    else:
                        state_hapiness[state] = tweetScore
                
                # end if state known
                
            # end if country code US
            
        # end if place data available
        
    # end for each tweet
    
    happiestVal = 0
    happiestState = 'UNKN'
    for stateVal in state_hapiness:
        hapinness = state_hapiness[stateVal]
        print stateVal + ' ' + str(state_hapiness[stateVal])
        if hapinness > happiestVal:
            happiestState = stateVal
            happiestVal = hapinness
    #this would just print out happiest
    #print happiestState
    
    #print '\nCan we order and get top 10?'
    
    # lets try and print out 10 happiest states in order, in json
    happyState = {}
    count = 1
    
    # in with default values, unknown fill
    for state in states:
        happyState[state] = {'score':'NA','rank':'NA', 'fillKey':'UNKNOWN'}
    
    # set date and filename used, remove str when going straight to mongo
    happyState['parseDate'] = datetime.datetime.today()
    happyState['fileName'] = sys.argv[2]
    happyState['hashtags'] = top_hashtags(sys.argv[2])
    
    for w in sorted(state_hapiness, key=state_hapiness.get, reverse=True):
        print w, float(state_hapiness[w])
        
        # formatting for datamaps
        fill = 'UNKNOWN'
        if count == 1:
            fill = 'TOP'
        elif (2 <= count and count <= 10):
            fill = 'HIGH'
        elif (11 <= count and count <= 25):
            fill = 'MEDIUM'
        elif (26 <= count and count <= 51):
            fill = 'LOW'
        
        happyState[w] = {'score':state_hapiness[w],'rank':count, 'fillKey':fill}
        count += 1
        #if count > 10:
        #    break

    #with open('happiest_states.json', 'w') as outfile:
    #    json.dump(happyState, outfile)
    
    # insert into local mongo
    client = MongoClient('localhost', 27017)
    db = client.twit_data
    sCol = db.happiest_states
    rec_id = sCol.insert(happyState)
    print 'Inserted into mongo, id: ' + str(rec_id)
            

# function to also compute top ten hashtags
def top_hashtags(filename):
    #print "hello there"

    tweet_file = open(filename)

    hash_counts = {}

    # Hashtags can be an array
    # entities['hashtags']:[]

    for line in tweet_file:

        lineData = {}
        try:
            lineData = json.loads(line)
        except:
            lineData = {}

        if 'entities' in lineData:
            entityObj = lineData['entities']
            if 'hashtags' in entityObj:
                hashtagsList = entityObj['hashtags']

                #print hashtagsObj
                for hashtagsObj in hashtagsList:

                    if 'text' in hashtagsObj:
                        hashtag = hashtagsObj['text']
                        hashtagStr = hashtag.encode('utf-8')
                        #print hashtagStr

                        if hashtagStr in hash_counts:
                            # get current count
                            curCount = hash_counts[hashtagStr]
                            curCount += 1
                            hash_counts[hashtagStr] = curCount
                        else:
                            # add initial count
                            hash_counts[hashtagStr] = 1


                # end for each
            # end if hashtags in entities
        # end if entities in tweet
    # end for each line of tweets

    # now we have total hashtag counts
    # need to find top ten

    #print hash_counts

    # lets try and sort
    # cool, found this on stackexchange...
    topTen = []
    count = 1
    for w in sorted(hash_counts, key=hash_counts.get, reverse=True):
        print w, float(hash_counts[w])
        topTen.append({'hashtag':w,'count':hash_counts[w]})
        count += 1
        if count > 10:
            break
    return topTen


if __name__ == '__main__':
    main()
