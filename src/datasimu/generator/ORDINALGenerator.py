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
    
    def getRandom(self,choice,bias):
        r=random.random()
        c= self.findBiasChoice(r,bias)
        return choice[c]
    
    def findBiasChoice(self,r,bias):
        i=0
        for c in bias:
            if r < c:
                return i
            else:
                i+=1
        return i