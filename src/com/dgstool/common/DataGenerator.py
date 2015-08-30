'''
Created on Aug 30, 2015

@author: Subhasis
'''

import xml.etree.ElementTree as ET

class DataGenerator(object):
    '''
    This does all the processing to take an XML input and create an output that is persisted.
    '''
    
    def __init__(self,fileName):
        '''
        Constructor
        '''
        self.inputConfigFile=fileName
        
    def processXMLConfig(self):
        '''
        This method parses a XML file and returns an Object that acts as the input for generating data.
        '''        
        tree = ET.parse(self.inputConfigFile)
        root = tree.getroot()
        print root        
        return root
    
    def generateData(self):  
        pass 
     
    def process(self):
        root=self.processXMLConfig()
        
        return True

