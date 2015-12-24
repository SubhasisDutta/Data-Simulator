'''
Created on Sep 6, 2015

@author: Subhasis
'''
import random
import string
import rstr


class STRINGGenerator(object):
    '''
    classdocs
    '''


    def __init__(self, dataConf):
        '''
        Constructor
        '''
        self.dataConf=dataConf
    
    def getRandom(self,choice):
        if self.dataConf.pattern == 'Random_normal':
            if self.dataConf.minimum is None and self.dataConf.maximum is None:
                return ''.join(random.SystemRandom().choice(choice) for _ in range(10))
            elif self.dataConf.maximum is None:
                return ''.join(random.SystemRandom().choice(choice) for _ in range(int(self.dataConf.minimum)))                       
            else:
                range_length=random.randint(int(self.dataConf.minimum),int(self.dataConf.maximum))
                return ''.join(random.SystemRandom().choice(choice) for _ in range(range_length))       
        elif self.dataConf.pattern == 'E_Mail':                                    
            return '{0}@{1}.{2}'.format(rstr.domainsafe(),rstr.domainsafe(),rstr.letters(3))
        elif self.dataConf.pattern == 'Postal_Address':                                    
            return """{0} {1} {2} {3} {4}, {5} {6} """.format(rstr.letters(4, 8).title(),rstr.letters(4, 8).title(),
                                                              rstr.digits(3, 5),rstr.letters(4, 10).title(),
                                                              rstr.letters(4, 15).title(),rstr.uppercase(2),rstr.digits(5))
        elif self.dataConf.pattern == 'User_Name':
            return '{0} {1}'.format(rstr.letters(4, 15).title(),rstr.letters(4, 10).title())  
        elif self.dataConf.pattern == 'Url_address':
            return 'http://{0}.{1}/{2}/?{3}'.format(rstr.domainsafe(),rstr.letters(3),rstr.urlsafe(),rstr.urlsafe())    
        else:
            return "XXXXX"