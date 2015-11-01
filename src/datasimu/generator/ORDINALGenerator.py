'''
Created on Sep 6, 2015

@author: Subhasis
'''
import random

class ORDINALGenerator(object):
    '''
    classdocs
    '''


    def __init__(self, dataConf):
        '''
        Constructor
        '''
        self.dataConf=dataConf
    
    def getRandom(self):
        count=len(self.dataConf.choice)
        c= random.randint(0,count-1)
        return self.dataConf.choice[c]