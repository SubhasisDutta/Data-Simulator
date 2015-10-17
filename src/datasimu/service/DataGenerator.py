'''
Created on Aug 30, 2015

@author: Subhasis
'''

import xml.etree.ElementTree as ET
import datetime
import random
from datasimu.validator.ConfigValidator import ConfigValidator
from datasimu.manager.CSVFileManager import CSVFileManager
from datasimu.manager.CassandraManager import CassandraManager
from datasimu.config.RandomConfig import RandomConfig
from datasimu.generator.IntegerGenrator import IntegerGenrator
from datasimu.generator.FloatGenrator import FloatGenrator
from datasimu.generator.DecimalGenrator import DecimalGenrator
from datasimu.service.TweetService import TweetService


class DataGenerator(object):
    '''
    This does all the processing to take an XML input and create an output that is persisted.
    '''
    
    def __init__(self,inputConfigFile):
        '''
        Constructor
        '''
        self.inputConfigFile=inputConfigFile   
        self.manager = None   
        self.generate = None
        
    def processXMLConfig(self):
        '''
        This method parses a XML file and returns an Object that acts as the input for generating data.
        '''        
        tree = ET.parse(self.inputConfigFile)
        root = tree.getroot()              
        return root
          
    def generateData(self,record):  
        #To do for other records
        try:        
            for column in self.root.findall('column'):
                dataConf=RandomConfig(column)
                value= None
                if dataConf.dataType == "Integer":                
                    value=IntegerGenrator(dataConf).getRandom()
                elif dataConf.dataType == "Float":
                    value=FloatGenrator(dataConf).getRandom()
                elif dataConf.dataType == "Decimal":
                    value=DecimalGenrator(dataConf).getRandom()
                elif dataConf.dataType == "Choice": #TODO : based on choice present selct
                    value=random.random()
                elif dataConf.dataType == "String": #TODO : based on string set available randomise 
                    value=random.random() 
                elif dataConf.dataType == "Tweet": #TODO : based on string set available randomise 
                    value=random.random()   
                else: # will be considered float (0,1]
                    value=random.random()                    
                #Process column information
                record.append(value) 
        except:
            #TO DO handle any error
            raise         
        return record    
   
    def getHeading(self):
        heading=[]
        heading.append(self.root.find('startindex').get('name'))
        for column in self.root.findall('column'):
            heading.append(column.get('name'))
        return heading
        
    def initiateManager(self):
        if self.outputMode == 'FILE':
            self.manager=CSVFileManager(self.root)
        elif self.outputMode == 'CASSANDRA':
            self.manager=CassandraManager(self.root)
        else:
            raise IOError
    
    def process(self):
        '''
        Parse the Config and generates the data
        '''
        '''
        This checks if the Configuration file is in correct format.
        '''
        configValidator=ConfigValidator()
        if not configValidator.valid(self.inputConfigFile):
            return False
        '''
        This loads the configuration into an object.
        '''
        self.root=self.processXMLConfig()
        
        self.outputFormat = self.root.find('resulttype').find('format').text
        self.outputMode= self.root.find('resulttype').find('mode').text
        
        self.initiateManager()
        
        specialtype=self.root.find('specialtype')
        
        if specialtype is None:
            self.manager.push(self.getHeading(),'wb')  
            startTime=datetime.datetime.strptime(self.root.find('startindex').text, "%Y-%m-%dT%H:%M:%S")
            endTime=datetime.datetime.strptime(self.root.find('endindex').text, "%Y-%m-%dT%H:%M:%S")
            timeIterator=startTime
            
            while timeIterator < endTime:
                record=[]            
                record.append(timeIterator) 
                self.manager.push(self.generateData(record))         
                timeIterator += self.getTimeDelta()
        elif specialtype.text == 'TweetGenerate':
            TweetService(self.manager,self.root).process()       
        else:
            return False
        return True

    def getTimeDelta(self):
        timeDelta=self.root.find('timedelta').text
        timedeltaunit=self.root.find('timedeltaunit').text
        #microseconds, milliseconds, seconds, minutes, hours, days, weeks
        if timedeltaunit == 'seconds':
            return datetime.timedelta(seconds=int(timeDelta))
        if timedeltaunit == 'milliseconds':
            return datetime.timedelta(milliseconds=int(timeDelta))
        if timedeltaunit == 'minutes':
            return datetime.timedelta(minutes=int(timeDelta))
        if timedeltaunit == 'hours':
            return datetime.timedelta(hours=int(timeDelta))
        if timedeltaunit == 'days':
            return datetime.timedelta(days=int(timeDelta))
        if timedeltaunit == 'weeks':
            return datetime.timedelta(weeks=int(timeDelta)) 
        return datetime.timedelta(seconds=int(timeDelta))
