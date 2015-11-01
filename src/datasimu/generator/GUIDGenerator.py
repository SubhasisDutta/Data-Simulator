'''
Created on Sep 6, 2015

@author: Subhasis
'''
import uuid

class GUIDGenerator(object):
    '''
    classdocs
    '''


    def __init__(self, dataConf):
        '''
        Constructor
        '''
        self.dataConf=dataConf
    
    def getRandom(self):
        return uuid.uuid1()