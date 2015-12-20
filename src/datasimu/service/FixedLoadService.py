'''
Created on Sep 23, 2015

@author: Subhasis
'''

import datetime
from random import randint
from datasimu.generator.RecordGenerator import RecordGenerator

class FixedLoadService(object):
    '''
    This will generate variable timestamp based record based on load patern.
    '''

    def __init__(self, manager,config):
        '''
        Constructor
        '''
        self.manager=manager
        self.config=config
        self.generator=RecordGenerator(self.config)
        
    def process(self):        
                       
        total_record = int(self.config.find('totalrecord').text)                 
        self.generateRecords(total_record)           
        self.manager.flushBatch()                
        
    def generateRecords(self,total_record):
        for i in range(total_record):                        
            self.manager.push(self.generator.generateDataCount(i)) 
        


        
                      
    
