'''
Created on Aug 30, 2015

@author: Subhasis
'''

import xml.etree.ElementTree as ET
from datasimu.validator.ConfigValidator import ConfigValidator
from datasimu.manager.CSVFileManager import CSVFileManager
from datasimu.manager.CassandraManager import CassandraManager
from datasimu.manager.MySqlManager import MySqlManager
from datasimu.service.UniformService import UniformService
from datasimu.service.LoadService import LoadService
from datasimu.service.FixedLoadService import FixedLoadService
from datasimu.manager.MongoDBManager import MongoDBManager

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
       
    def getHeading(self):
        heading=[]        
        for column in self.root.findall('column'):
            heading.append(column.get('name'))
        return heading
        
    def initiateManager(self):
        if self.outputMode == 'FILE':
            self.manager=CSVFileManager(self.root)
            self.manager.push(self.getHeading(),'wb')
        elif self.outputMode == 'CASSANDRA':
            self.manager=CassandraManager(self.root)
        elif self.outputMode == 'MYSQL':
            self.manager=MySqlManager(self.root)
        elif self.outputMode == 'MONGODB':
            self.manager=MongoDBManager(self.root)
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
        
        specialtype=self.root.find('timesliceType')
        
        if specialtype is None or specialtype.text == 'UNIFORM':
            UniformService(self.manager,self.root).process()
        elif specialtype.text == 'LOAD_GENERATE':
            LoadService(self.manager,self.root).process()
        elif specialtype.text == 'FIXED_LOAD':
            FixedLoadService(self.manager,self.root).process()      
        else:
            return False
        return True