'''
Created on Sep 6, 2015

@author: Subhasis
'''
import random

class BOOLEANGenerator(object):
    '''
    classdocs
    '''
    def __init__(self, dataConf):
        '''
        Constructor
        '''
        self.dataConf=dataConf
    
    def getRandom(self):
        return random.random() < 0.5