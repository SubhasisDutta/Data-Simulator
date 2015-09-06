'''
Created on Sep 6, 2015

@author: Subhasis
'''

import csv

class CSVFileManager(object):
    '''
    This class takes care of writing the results into a csv file.
    '''


    def __init__(self, config):
        '''
        Constructor
        '''
        self.config=config
        self.resultFile=self.config.find('resulttype').find('location').text
        
    def push(self,dataList,writeType):
        with open(self.resultFile, writeType) as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(dataList)
        return True