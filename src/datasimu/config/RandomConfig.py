'''
Created on Sep 6, 2015

@author: Subhasis
'''

class RandomConfig(object):
    '''
    classdocs
    '''
    def __init__(self, column):
        '''
        Constructor
        '''
        self.dataType = column.findtext('datatype',default='FLOAT')
        self.pattern=column.findtext('pattern',default='Random_normal')
        self.minimum=column.findtext('minimum',default=None)
        self.maximum=column.findtext('maximum',default=None)
        self.step=column.findtext('step',default=None)
        self.mean=column.findtext('mean',default=None)
        self.stdev=column.findtext('stdev',default=None)
        self.slope=column.findtext('slope',default=None)
        if self.dataType == "STRING":
            if self.minimum is None:
                self.minimum = column.findtext('fixed',default=None)
        self.unit =column.findtext('unit',default=None)
            
