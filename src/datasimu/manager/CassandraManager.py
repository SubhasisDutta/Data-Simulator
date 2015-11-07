'''
Created on Sep 16, 2015

@author: Subhasis
'''

from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
import uuid
from datetime import datetime
import time
from cassandra.query import BatchStatement, SimpleStatement

class CassandraManager(object):
    '''
    This class takes care of writing the results into a cassandra file.
    '''
    def __init__(self, config):
        '''
        Constructor
        '''
        self.config=config        
        self.keyspace=self.config.find('resulttype').find('keyspace').text
        self.resultTable=self.config.find('resulttype').find('table').text
        self.batchSize=int(self.config.find('resulttype').find('batchsize').text)
        self.cluster = Cluster(self.getNodesInCluster())
        self.session = self.cluster.connect(self.keyspace)
        self.dbColumnList=self.getDBColumnNames() 
        self.dbColumnNames=self.getdbColString()
        self.insertPoints=self.getInsertPointString()
        self.insertBatch= BatchStatement()
        self.batchCount=0
        self.insertQuery=self.session.prepare('INSERT INTO '+self.resultTable+' ("id",'+self.dbColumnNames+') VALUES ('+self.insertPoints+')')
        
    def getdbColString(self):
        dbColumnNames=','
        return self.config.find('startindex').get('dbColumnName')+','+dbColumnNames.join(self.dbColumnList)
               
    def getInsertPointString(self):
        insertPoints='?,?,'        
        for i in range(len(self.dbColumnList)):
            insertPoints+="?,"
        return insertPoints[:-1]
    
    def getNodesInCluster(self):
        clusterNodes=[]
        for clusterNode in self.config.find('resulttype').find('clusters').findall('cluser'):
            clusterNodes.append(clusterNode.text)        
        return clusterNodes
    
    def getDBColumnNames(self):
        dbCols=[]
        for column in self.config.findall('column'):
            dbCols.append(column.get('dbColumnName'))
        return dbCols
    
    def push(self,dataList,writeType='ab'):        
#         insertStatement ='INSERT INTO '+self.resultTable+' ("id",'+self.dbColumnNames+') VALUES ('+self.insertPoints+')'                  
#         dataList[0]=dataList[0].strftime("%Y-%m-%d %H:%M:%S")
        dataList.insert(0,uuid.uuid1())        
#         self.session.execute(insertStatement, dataList)        
        return self.batchQuery(self.insertQuery, dataList)
    
    def batchQuery(self,statement,dataList):
        if self.batchCount < self.batchSize: 
            self.insertBatch.add(statement,dataList)
            self.batchCount +=1
        else:
            self.insertBatch.add(statement,dataList)
            self.session.execute(self.insertBatch)
            self.batchCount =0
            self.insertBatch= BatchStatement()
        return True
    
    def flushBatch(self):
        self.session.execute(self.insertBatch)
        return True
            