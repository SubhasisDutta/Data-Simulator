'''
Created on Sep 6, 2015

@author: Subhasis
'''
import random
import string

class STRINGGenerator(object):
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
            if self.dataConf.minimum is None and self.dataConf.maximum is None:
                return ''.join(random.SystemRandom().choice(self.dataConf.choice) for _ in range(10))
            elif self.dataConf.maximum is None:
                return ''.join(random.SystemRandom().choice(self.dataConf.choice) for _ in range(int(self.dataConf.minimum)))                       
            else:
                range_length=random.randint(int(self.dataConf.minimum),int(self.dataConf.maximum))
                return ''.join(random.SystemRandom().choice(self.dataConf.choice) for _ in range(range_length))       
        else:
            return "XXXXX"