'''
Created on Sep 6, 2015

@author: Subhasis
'''
import string

class RandomConfig(object):
    '''
    classdocs
    '''


    def __init__(self, column):
        '''
        Constructor
        '''
        #args -- tuple of anonymous arguments
        #kwargs -- dictionary of named arguments
        self.dataType = column.findtext('datatype',default='Float')
        self.pattern=column.findtext('pattern',default='Random_normal')
        self.minimum=column.findtext('minimum',default=None)
        self.maximum=column.findtext('maximum',default=None)
        self.step=column.findtext('step',default=None)
        self.mean=column.findtext('mean',default=None)
        self.stdev=column.findtext('stdev',default=None)
        self.slope=column.findtext('slope',default=None)
        self.choice=None
        if self.dataType == "ORDINAL":
            self.choice=self.loadAllChoice(column.find('choice'))
        elif self.dataType == "STRING":
            if self.minimum is None:
                self.minimum = column.findtext('fixed',default=None)
            self.choice=self.loadStringChoice(column.find('choice'))
        self.unit =column.findtext('unit',default=None)
        
    def loadAllChoice(self,choice):
        options=[]        
        seed=choice.get('seed',default=None)
        if seed is not None:
            with open(seed) as f:
                options=f.read().splitlines()            
        else:
            for opt in choice.findall('option'):
                options.append(opt.text)        
        return options
    
    def loadStringChoice(self,choice):        
        if choice is None:
            return string.digits+string.uppercase+string.lowercase            
        else:
            s=""
            for opt in choice.findall('option'):
                if opt.text == "digits":
                    s+=string.digits
                elif opt.text == "hexdigits": 
                    s+=string.hexdigits
                elif opt.text == "lowercase": 
                    s+=string.lowercase
                elif opt.text == "octdigits": 
                    s+=string.octdigits
                elif opt.text == "punctuation": 
                    s+=string.punctuation
                elif opt.text == "uppercase": 
                    s+=string.uppercase
                elif opt.text == "whitespace": 
                    s+=string.whitespace    
            return s