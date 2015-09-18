'''
Created on Sep 16, 2015

@author: Subhasis
'''

from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
import uuid
from datetime import datetime
import time

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
        self.cluster = Cluster(self.getNodesInCluster())
        self.session = self.cluster.connect(self.keyspace)
        self.dbColumnList=self.getDBColumnNames() 
        self.dbColumnNames=self.getdbColString()
        self.insertPoints=self.getInsertPointString()
        
    def getdbColString(self):
        dbColumnNames=','
        return self.config.find('startindex').get('dbColumnName')+','+dbColumnNames.join(self.dbColumnList)
               
    def getInsertPointString(self):
        insertPoints='%s,%s,'        
        for i in range(len(self.dbColumnList)):
            insertPoints+="%s,"
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
    
    def push(self,dataList,writeType):        
        insertStatement ='INSERT INTO '+self.resultTable+' ("id",'+self.dbColumnNames+') VALUES ('+self.insertPoints+')'                  
        dataList[0]=dataList[0].strftime("%Y-%m-%d %H:%M:%S")
        dataList.insert(0,uuid.uuid1())        
        self.session.execute(insertStatement, dataList)
        return True