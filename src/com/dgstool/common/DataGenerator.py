'''
Created on Aug 30, 2015

@author: Subhasis
'''

import xml.etree.ElementTree as ET
import csv
import datetime

class DataGenerator(object):
    '''
    This does all the processing to take an XML input and create an output that is persisted.
    '''
    
    def __init__(self,inputConfigFile,resultFile):
        '''
        Constructor
        '''
        self.inputConfigFile=inputConfigFile
        self.resultFile=resultFile
        
    def processXMLConfig(self):
        '''
        This method parses a XML file and returns an Object that acts as the input for generating data.
        '''        
        tree = ET.parse(self.inputConfigFile)
        root = tree.getroot()              
        return root
    
    def generateData(self,confObj):  
        pass 
    
    def insertToCSVFile(self,dataList,writeType):
        with open(self.resultFile, writeType) as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(dataList)
        return True
   
    def getHeading(self):
        heading=[]
        heading.append(self.root.find('startindex').get('name'))
        for column in self.root.findall('column'):
            heading.append(column.get('name'))
        return heading
        
    def process(self):
        '''
        Parcs the Config and generates the data
        '''
        self.root=self.processXMLConfig()
        self.insertToCSVFile(self.getHeading(),'wb')
        
        print self.root.find('startindex').text
        
        startTime=datetime.datetime.strptime(self.root.find('startindex').text, "%Y-%m-%dT%H:%M:%S")
        endTime=datetime.datetime.strptime(self.root.find('endindex').text, "%Y-%m-%dT%H:%M:%S")
        timeIterator=startTime
        count=1
        while timeIterator < endTime:
            record=[]
            record.append(timeIterator)
            #To do for other records
            record.append('A random'+str(count))
            record.append('B random'+str(count))
            record.append('C random'+str(count))
            count+=1
            timeIterator += datetime.timedelta(milliseconds=int(self.root.find('step').text))            
            self.insertToCSVFile(record,'ab')        
        return True

