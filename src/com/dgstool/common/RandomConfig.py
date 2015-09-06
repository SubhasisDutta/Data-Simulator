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
        self.choice=column.findtext('choice',default=None)
        self.unit =column.findtext('unit',default=None)