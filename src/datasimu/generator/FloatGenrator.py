'''
Created on Sep 6, 2015

@author: Subhasis
'''
import random
import numpy as np

class FloatGenrator(object):
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
            if self.dataConf.minimum is None or self.dataConf.maximum is None:
                return random.random()
            elif self.dataConf.minimum != 0 or self.dataConf.minimum != 1 and float(self.dataConf.mean) is None:
                return random.uniform(float(self.dataConf.minimum),float(self.dataConf.maximum))
            elif self.dataConf.minimum is not None or self.dataConf.minimum is not None and float(self.dataConf.mean) is not None:
                return random.triangular(float(self.dataConf.minimum),float(self.dataConf.maximum),float(self.dataConf.mean))
            else:
                return random.random()
        elif self.dataConf.pattern == 'Standard_Deviation':
            if self.dataConf.mean is not None and self.dataConf.stdev is not None:
                return np.random.normal(float(self.dataConf.mean),float(self.dataConf.stdev))
            else:
                return 0
        else:
            return random.random()