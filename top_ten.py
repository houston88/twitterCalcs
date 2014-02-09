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
    count = 1
    for w in sorted(hash_counts, key=hash_counts.get, reverse=True):
        print w, float(hash_counts[w])
        count += 1
        if count > 10:
            break
    
    

if __name__ == '__main__':
    main()