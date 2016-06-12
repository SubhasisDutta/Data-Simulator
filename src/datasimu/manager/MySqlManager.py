'''
Created on Sep 16, 2015

@author: Subhasis
'''
import mysql.connector

class MySqlManager(object):
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
        self.schema=self.config.find('resulttype').find('schema').text
        self.resultTable=self.config.find('resulttype').find('table').text
        self.batchSize=int(self.config.find('resulttype').find('batchsize').text)
        self.cluster = self.getNodesInCluster()
        self.connection = mysql.connector.connect(host=self.cluster[0],
                        user=self.username,
                        passwd=self.password,
                        db=self.schema)
        self.dbColumnList=self.getDBColumnNames()
        self.insertPoints=self.getInsertPointString()
        self.insertBatch= []
        self.batchCount=0        
        columnstr = ','.join(self.dbColumnList)             
        self.insertQuery='INSERT INTO '+self.resultTable+' ('+columnstr+') VALUES ('+self.insertPoints+')' 
#         self.createTableIfNotExist()
    
    def createTableIfNotExist(self):
        cursor=self.connection.cursor()
        
        createString='CREATE TABLE IF NOT EXISTS '+self.resultTable+' (<column definitions>)'
        cursor.execute(createString)        
                        
    def getInsertPointString(self):
        insertPoints=''        
        for i in range(len(self.dbColumnList)):
            insertPoints+="%s,"
        return insertPoints[:-1]
    
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
        return self.batchQuery(self.insertQuery, dataList)
    
    def batchQuery(self,statement,dataList):
        if self.batchCount < self.batchSize:
            self.insertBatch.append(tuple(dataList))
            self.batchCount +=1
        else:
            self.insertBatch.append(tuple(dataList))
            cursor=self.connection.cursor()
            cursor.executemany(self.insertQuery,self.insertBatch)
            self.batchCount =0
            self.connection.commit()
            self.insertBatch= []
        return True
    
    def flushBatch(self):
        cursor=self.connection.cursor()
        cursor.executemany(self.insertQuery,self.insertBatch)
        self.batchCount =0
        self.connection.commit()
        self.insertBatch= []
        return True
            