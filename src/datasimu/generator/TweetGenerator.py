'''
Created on Oct 17, 2015

@author: Subhasis
'''
   
import csv 
import random
    
class TweetGenerator(object):
    '''
    classdocs
    '''

    def __init__(self, config):
        '''
        Constructor
        '''
        self.config=config
        #loads the tweet seed data
        self.seed_authors,self.seed_tweets=self.loadTweetSeed(self.config.find('tweetload').find('tweetseed').text)
    
    def getRandomTweetRecord(self,record):
        #get random author
        record.append(random.choice(self.seed_authors))
        #get random tweet
        record.append(random.choice(self.seed_tweets)) 
        return record      
       
    def loadTweetSeed(self,file_path):
        author_row=int(self.config.find('tweetload').find('seedauthor').text)-1
        tweet_row=int(self.config.find('tweetload').find('seedtweet').text)-1                        
        authors=[]
        tweets =[]     
        try:
            with open(file_path, 'rb') as f:
                reader = csv.reader(f, delimiter=',')                
                for row in reader:                    
                    authors.append(row[author_row])
                    tweets.append(row[tweet_row])                
        except csv.Error as e:
            print "Seed file not found"
            raise e
        authors=list(set(authors[1:]))
        tweets=list(set(tweets[1:]))
        return authors,tweets 