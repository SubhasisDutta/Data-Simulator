'''
Created on Sep 23, 2015

@author: Subhasis
'''

import datetime
from random import randint
from datasimu.generator.TweetGenerator import TweetGenerator

class TweetService(object):
    '''
    This will generate Tweets based on seed Author and tweets and push data to storege of choice.
    '''

    def __init__(self, manager,config):
        '''
        Constructor
        '''
        self.manager=manager
        self.config=config
        self.generator=TweetGenerator(self.config)
        
    def process(self):
        startTime=datetime.datetime.strptime(self.config.find('tweetload').find('startindex').text, "%Y-%m-%dT%H:%M:%S")
                       
        totaltweet = int(self.config.find('tweetload').find('totaltweet').text)
        patternrepeat = int(self.config.find('tweetload').find('patternrepeat').text)
        patternrepeatunit = self.config.find('tweetload').find('patternrepeatunit').text               
        perloadCount=totaltweet/patternrepeat
                
        for i in range(patternrepeat):            
            self.processSinglePattern(startTime+(i*datetime.timedelta(seconds=self.getPatternSeconds(patternrepeatunit))),perloadCount,patternrepeatunit)
    
    def processSinglePattern(self,startTime,perloadCount,patternrepeatunit):        
        #This gets the distribution in the time interval        
        loadDistribution= self.getLoadDistibutionCount(perloadCount,self.getPaternRange(patternrepeatunit),self.config.find('tweetload').find('patternloaddistribution'))        
        second_distribution=[]
        for tweet_count in loadDistribution:
            second_distribution.append(self.generateSecondDistribution(tweet_count,self.getPatternUnitSeconds(patternrepeatunit)))        
        
        t=startTime                
        for i,sd in enumerate(second_distribution):
            keys=sorted(sd, key=sd.get)
            for key in keys:
                self.generateTweets(t+datetime.timedelta(seconds=key), sd[key])
            t+= datetime.timedelta(seconds=int(self.getPatternUnitSeconds(patternrepeatunit)))
            print "Tweets done for : %s - Twets added %s" %(t,loadDistribution[i])
           
        
    def generateTweets(self,timestamp,numbers):
        for i in range(numbers):
            record=[] 
            record.append(timestamp)            
            self.manager.push(self.generator.getRandomTweetRecord(record)) 

    def generateSecondDistribution(self,tweet_count,seconds_in_distribution):
        random_delta=int(tweet_count/1000)
        if random_delta == 0:
            random_delta=1
        tweets_left=tweet_count
        d={}
        while tweets_left > 0:
            r=randint(1,random_delta)
            s=randint(0,seconds_in_distribution-1)
            if s in d:
                d[s] += r
            else:
                d[s] = r
            tweets_left-=r        
        return d 
        
    def getLoadDistibutionCount(self,perload_count,pattern_range,load_distribution_config):
        load_distribution=[]
        load_total=0
        for pattern_range in load_distribution_config.findall('range'):
            load_total+=float(pattern_range.get('load'))
        normalize_factor=1/(load_total/100)
        
        for pattern_range in load_distribution_config.findall('range'):
            start_dist=int(pattern_range.get('start'))
            end_dist=int(pattern_range.get('end'))
            load= (normalize_factor * float(pattern_range.get('load')))/100
            distribution_count=perload_count*load
            for i in range(abs(end_dist-start_dist)):
                load_distribution.append(int(distribution_count/(abs(end_dist-start_dist))))
        
        return load_distribution                       
    
    def getPatternSeconds(self,patternrepeatunit):  
        if patternrepeatunit == "day":
            return 86400
        elif patternrepeatunit == "hour":
            return 3600
        elif patternrepeatunit == "week":
            return 604800
        elif patternrepeatunit == "month":
            return 2592000
        else:
            return 1
            
    def getPatternUnitSeconds(self,patternrepeatunit):  
        if patternrepeatunit == "day":
            return 3600
        elif patternrepeatunit == "hour":
            return 60
        elif patternrepeatunit == "week":
            return 86400
        elif patternrepeatunit == "month":
            return 86400
        else:
            return 1   
    
    def getPaternRange(self,patternrepeatunit):
        if patternrepeatunit == "day":
            return 24
        elif patternrepeatunit == "hour":
            return 60
        elif patternrepeatunit == "week":
            return 7
        elif patternrepeatunit == "month":
            return 30
        else:
            return 1  