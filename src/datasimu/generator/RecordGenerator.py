'''
Created on Oct 17, 2015

@author: Subhasis
'''
   
import csv 
import random
import string
from datasimu.config.RandomConfig import RandomConfig
from datasimu.generator.IntegerGenrator import IntegerGenrator
from datasimu.generator.FloatGenrator import FloatGenrator
from datasimu.generator.DecimalGenrator import DecimalGenrator
from datasimu.generator.GUIDGenerator import GUIDGenerator
from datasimu.generator.ORDINALGenerator import ORDINALGenerator
from datasimu.generator.BOOLEANGenerator import BOOLEANGenerator
from datasimu.generator.STRINGGenerator import STRINGGenerator

class RecordGenerator(object):
    '''
    classdocs
    '''
    def __init__(self, config):
        '''
        Constructor
        '''
        self.config=config
        self.ordinalChoice=self.loadOrdinalChoice()
        self.stringChoice=self.loadStringChoice()
    
    def generateData(self,timeStamp):  
        record=[]
        #To do for other records
        try:        
            for column in self.config.findall('column'):
                dataConf=RandomConfig(column)
                value= None
                if dataConf.dataType == "INTEGER":                
                    value=IntegerGenrator(dataConf).getRandom()
                elif dataConf.dataType == "FLOAT":
                    value=FloatGenrator(dataConf).getRandom()
                elif dataConf.dataType == "DECIMAL":
                    value=DecimalGenrator(dataConf).getRandom()
                elif dataConf.dataType == "GUID":
                    value=GUIDGenerator(dataConf).getRandom()
                elif dataConf.dataType == "ORDINAL": 
                    value=ORDINALGenerator(dataConf).getRandom(self.ordinalChoice[column.get('name')])
                elif dataConf.dataType == "BOOLEAN": 
                    value=BOOLEANGenerator(dataConf).getRandom()
                elif dataConf.dataType == "STRING":                     
                    value=STRINGGenerator(dataConf).getRandom(self.stringChoice[column.get('name')])
                elif dataConf.dataType == "TIMESTAMP":
                    value=timeStamp   
                else: # will be considered float (0,1]
                    value=random.random()                    
                #Process column information
                record.append(value) 
        except:
            #TO DO handle any error
            raise         
        return record
 
    def loadStringChoice(self):
        choicedict={}        
        for column in self.config.findall('column'):
            if "STRING" == column.findtext('datatype',default=None):  
                choice=column.find('choice')
                if choice is None:
                    choicedict[column.get('name')] = string.digits+string.uppercase+string.lowercase            
                else:
                    s=""
                    for opt in choice.findall('option'):
                        if opt.text == "digits":
                            s+=string.digits
                        elif opt.text == "hexdigits": 
                            s+=string.hexdigits
                        elif opt.text == "lowercase": 
                            s+=string.lowercase
                        elif opt.text == "octdigits": 
                            s+=string.octdigits
                        elif opt.text == "punctuation": 
                            s+=string.punctuation
                        elif opt.text == "uppercase": 
                            s+=string.uppercase
                        elif opt.text == "whitespace": 
                            s+=string.whitespace
                    choicedict[column.get('name')]=s
        return choicedict
    
    def loadOrdinalChoice(self):
        choicedict={}
        for column in self.config.findall('column'):              
            if "ORDINAL" == column.findtext('datatype',default=None):  
                options=[]
                choice=column.find('choice')
                seed=choice.get('seed',default=None)
                if seed is not None:
                    with open(seed) as f:
                        options=f.read().splitlines()            
                else:
                    for opt in choice.findall('option'):
                        options.append(opt.text)        
                choicedict[column.get('name')]= options
        #loads the tweet seed data
#       self.seed_authors,self.seed_tweets=self.loadTweetSeed(self.config.find('tableload').find('seed').text)        
        return choicedict  

#     def loadTweetSeed(self,file_path):
#         author_row=int(self.config.find('tableload').find('seedauthor').text)-1
#         tweet_row=int(self.config.find('tableload').find('seedtweet').text)-1                        
#         authors=[]
#         tweets =[]     
#         try:
#             with open(file_path, 'rb') as f:
#                 reader = csv.reader(f, delimiter=',')                
#                 for row in reader:                    
#                     authors.append(row[author_row])
#                     tweets.append(row[tweet_row])                
#         except csv.Error as e:
#             print "Seed file not found"
#             raise e
#         authors=list(set(authors[1:]))
#         tweets=list(set(tweets[1:]))
#         return authors,tweets 