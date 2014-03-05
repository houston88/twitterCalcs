#!/usr/bin/env python
'''
Created on May 13, 2013
@author: Houston Harris
'''

import sys
import string
import json

def main():
    #print "hello there"
    
    tweet_file = open(sys.argv[1])
    
    hash_counts = {}
    
    # Hashtags can be an array
    # entities['hashtags']:[]
    
    for line in tweet_file:
        
        lineData = {}
        try:
            lineData = json.loads(line)
        except:
            lineData = {}
        
        if 'place' in lineData and lineData['place']:
            # we have a place, lets print the place data
            placeData = lineData['place']
            
            if (placeData['country_code'] and placeData['country_code']=='US'):
                # only usa tweets to get insight into happiest states
                
                placeStr = 'UNKN'
                if 'place_type' in placeData:
                    # lets also store off place data for reference
                    placeStr = placeData['full_name'].encode('utf-8')
                
                if 'entities' in lineData:
                    entityObj = lineData['entities']
                    if 'hashtags' in entityObj:
                        hashtagsList = entityObj['hashtags']
                        
                        #print hashtagsObj
                        for hashtagsObj in hashtagsList:
                            
                            if 'text' in hashtagsObj:
                                hashtag = hashtagsObj['text']
                                hashtagStr = hashtag.encode('utf-8')
                                
                                # lets see what full text looks like
                                line_txt = lineData['text']
                                str_txt = line_txt.encode('utf-8')

                                print str_txt
                                print placeStr, placeData['country']
                                
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
            # end if pace in US
        # end if place data exists
    # end for each line of tweets
    
    # now we have total hashtag counts
    # need to find top ten
    
    #print hash_counts
    
    # lets try and sort
    # cool, found this on stackexchange...
    count = 1
    for w in sorted(hash_counts, key=hash_counts.get, reverse=True):
        print w, float(hash_counts[w])
        count += 1
        if count > 10:
            break
    
    

if __name__ == '__main__':
    main()