'''
Created on Sep 6, 2015

@author: Subhasis
'''
import random
import numpy as np

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
        elif self.dataConf.pattern == 'Standard_Deviation':
            if self.dataConf.mean is not None and self.dataConf.stdev is not None:
                return int(np.random.normal(int(self.dataConf.mean),int(self.dataConf.stdev)))
            else:
                return 0
        else:
            return 0