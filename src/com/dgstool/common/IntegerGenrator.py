'''
Created on Sep 6, 2015

@author: Subhasis
'''
import random

class IntegerGenrator(object):
    '''
    classdocs
    '''


    def __init__(self, dataConf):
        '''
        Constructor
        '''
        self.dataConf=dataConf
    
    def getRandom(self):
        if self.dataConf.pattern == 'Random_normal':
            if self.dataConf.step is None:
                return random.randint(int(self.dataConf.minimum),int(self.dataConf.maximum))
            else:
                return random.randrange(int(self.dataConf.minimum),int(self.dataConf.maximum),int(self.dataConf.step))                 
        else:
            return 0