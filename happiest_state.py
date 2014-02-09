'''
Created on May 13, 2013
@author: user
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
    
    # lets define state centers, just pick closest one using diff of lat/long
    stateCenters = {}
    stateCenters['AK'] = {'lat':61.3850,'long':-152.2683}
    stateCenters["AL"] = {'lat':32.7990,'long':-86.8073}
    stateCenters["AR"] = {'lat':34.9513,'long':-92.3809}
    stateCenters["AS"] = {'lat':14.2417,'long':-170.7197}
    stateCenters["AZ"] = {'lat':33.7712,'long':-111.3877}
    stateCenters["CA"] = {'lat':36.1700,'long':-119.7462}
    stateCenters["CO"] = {'lat':39.0646,'long':-105.3272}
    stateCenters["CT"] = {'lat':41.5834,'long':-72.7622}
    stateCenters["DC"] = {'lat':38.8964,'long':-77.0262}
    stateCenters["DE"] = {'lat':39.3498,'long':-75.5148}
    stateCenters["FL"] = {'lat':27.8333,'long':-81.7170}
    stateCenters["GA"] = {'lat':32.9866,'long':-83.6487}
    stateCenters["HI"] = {'lat':21.1098,'long':-157.5311}
    stateCenters["IA"] = {'lat':42.0046,'long':-93.2140}
    stateCenters["ID"] = {'lat':44.2394,'long':-114.5103}
    stateCenters["IL"] = {'lat':40.3363,'long':-89.0022}
    stateCenters["IN"] = {'lat':39.8647,'long':-86.2604}
    stateCenters["KS"] = {'lat':38.5111,'long':-96.8005}
    stateCenters["KY"] = {'lat':37.6690,'long':-84.6514}
    stateCenters["LA"] = {'lat':31.1801,'long':-91.8749}
    stateCenters["MA"] = {'lat':42.2373,'long':-71.5314}
    stateCenters["MD"] = {'lat':39.0724,'long':-76.7902}
    stateCenters["ME"] = {'lat':44.6074,'long':-69.3977}
    stateCenters["MI"] = {'lat':43.3504,'long':-84.5603}
    stateCenters["MN"] = {'lat':45.7326,'long':-93.9196}
    stateCenters["MO"] = {'lat':38.4623,'long':-92.3020}
    stateCenters["MP"] = {'lat':14.8058,'long':145.5505}
    stateCenters["MS"] = {'lat':32.7673,'long':-89.6812}
    stateCenters["MT"] = {'lat':46.9048,'long':-110.3261}
    stateCenters["NC"] = {'lat':35.6411,'long':-79.8431}
    stateCenters["ND"] = {'lat':47.5362,'long':-99.7930}
    stateCenters["NE"] = {'lat':41.1289,'long':-98.2883}
    stateCenters["NH"] = {'lat':43.4108,'long':-71.5653}
    stateCenters["NJ"] = {'lat':40.3140,'long':-74.5089}
    stateCenters["NM"] = {'lat':34.8375,'long':-106.2371}
    stateCenters["NV"] = {'lat':38.4199,'long':-117.1219}
    stateCenters["NY"] = {'lat':42.1497,'long':-74.9384}
    stateCenters["OH"] = {'lat':40.3736,'long':-82.7755}
    stateCenters["OK"] = {'lat':35.5376,'long':-96.9247}
    stateCenters["OR"] = {'lat':44.5672,'long':-122.1269}
    stateCenters["PA"] = {'lat':40.5773,'long':-77.2640}
    stateCenters["PR"] = {'lat':18.2766,'long':-66.3350}
    stateCenters["RI"] = {'lat':41.6772,'long':-71.5101}
    stateCenters["SC"] = {'lat':33.8191,'long':-80.9066}
    stateCenters["SD"] = {'lat':44.2853,'long':-99.4632}
    stateCenters["TN"] = {'lat':35.7449,'long':-86.7489}
    stateCenters["TX"] = {'lat':31.1060,'long':-97.6475}
    stateCenters["UT"] = {'lat':40.1135,'long':-111.8535}
    stateCenters["VA"] = {'lat':37.7680,'long':-78.2057}
    stateCenters["VI"] = {'lat':18.0001,'long':-64.8199}
    stateCenters["VT"] = {'lat':44.0407,'long':-72.7093}
    stateCenters["WA"] = {'lat':47.3917,'long':-121.5708}
    stateCenters["WI"] = {'lat':44.2563,'long':-89.6385}
    stateCenters["WV"] = {'lat':38.4680,'long':-80.9696}
    stateCenters["WY"] = {'lat':42.7475,'long':-107.2085}
    
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
                    
                    if placeTypeStr == 'city':
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
    count = 1
    happyState = {}
    
    # set date and filename used, remove str when going straight to mongo
    happyState['parseDate'] = datetime.datetime.today()
    happyState['fileName'] = sys.argv[2]
    
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
    #  json.dump(happyState, outfile)
    
    # insert into local mongo
    client = MongoClient('localhost', 27017)
    db = client.twit_data
    sCol = db.happiest_states
    rec_id = sCol.insert(happyState)
    print 'Inserted into mongo, id: ' + str(rec_id)
            

if __name__ == '__main__':
    main()