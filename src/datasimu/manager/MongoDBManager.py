'''
Created on Sep 16, 2015

@author: Subhasis
'''
import pymongo
from pymongo.mongo_client import MongoClient


class MongoDBManager(object):
    '''
    This class takes care of writing the results into a mysql table.
    '''
    def __init__(self, config):
        '''
        Constructor
        '''
        self.config=config   
        self.username=self.config.find('resulttype').find('username').text
        self.password=self.config.find('resulttype').find('password').text      
        self.schema=self.config.find('resulttype').find('schema').text #database
        self.resultTable=self.config.find('resulttype').find('table').text #collection
        self.batchSize=int(self.config.find('resulttype').find('batchsize').text)
        self.port=int(self.config.find('resulttype').find('port').text)
        self.client=MongoClient(self.getNodesInCluster()[0],self.port)
        self.db=self.client[self.schema]
        self.collection=self.db[self.resultTable]        
        self.dbColumnList=self.getDBColumnNames()                
        self.insertBatch= []
        self.batchCount=0                           

                        
    def getInsertQuery(self,data):                
        d={}
        for i in range(len(self.dbColumnList)):
            d[self.dbColumnList[i]]=data[i]
        return d
    
    def getNodesInCluster(self):
        clusterNodes=[]
        for clusterNode in self.config.find('resulttype').find('clusters').findall('host'):
            clusterNodes.append(clusterNode.text)        
        return clusterNodes
    
    def getDBColumnNames(self):
        dbCols=[]
        for column in self.config.findall('column'):
            dbCols.append(column.get('dbColumnName'))
        return dbCols
    
    def push(self,dataList,writeType='ab'):        
        return self.batchQuery(dataList)
    
    def batchQuery(self,dataList):
        if self.batchCount < self.batchSize:
            data_dict=self.getInsertQuery(dataList)
            self.insertBatch.append(data_dict)
            self.batchCount +=1
        else:
            data_dict=self.getInsertQuery(dataList)
            self.insertBatch.append(data_dict)
            self.collection.insert_many(self.insertBatch)            
            self.batchCount =0
            self.insertBatch= []
        return True
    
    def flushBatch(self):        
        self.collection.insert_many(self.insertBatch)
        self.batchCount =0
        self.insertBatch= []
        return True
            