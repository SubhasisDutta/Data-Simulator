'''
Created on Oct 17, 2015

@author: Subhasis
'''
   
import csv 
import random
import string
from datasimu.config.RandomConfig import RandomConfig
from datasimu.generator.IntegerGenrator import IntegerGenrator
from datasimu.generator.FloatGenrator import FloatGenrator
from datasimu.generator.DecimalGenrator import DecimalGenrator
from datasimu.generator.GUIDGenerator import GUIDGenerator
from datasimu.generator.ORDINALGenerator import ORDINALGenerator
from datasimu.generator.BOOLEANGenerator import BOOLEANGenerator
from datasimu.generator.STRINGGenerator import STRINGGenerator

class RecordGenerator(object):
    '''
    classdocs
    '''
    def __init__(self, config):
        '''
        Constructor
        '''
        self.config=config
        self.ordinalChoice,self.odinalBias=self.loadOrdinalChoice()
        self.stringChoice=self.loadStringChoice()
    
    def generateData(self,timeStamp):  
        record=[]
        #To do for other records
        try:        
            for column in self.config.findall('column'):
                dataConf=RandomConfig(column)
                value= None
                if dataConf.dataType == "INTEGER":                
                    value=IntegerGenrator(dataConf).getRandom()
                elif dataConf.dataType == "FLOAT":
                    value=FloatGenrator(dataConf).getRandom()
                elif dataConf.dataType == "DECIMAL":
                    value=DecimalGenrator(dataConf).getRandom()
                elif dataConf.dataType == "GUID":
                    value=GUIDGenerator(dataConf).getRandom()
                elif dataConf.dataType == "ORDINAL": 
                    value=ORDINALGenerator(dataConf).getRandom(self.ordinalChoice[column.get('name')],self.odinalBias[column.get('name')])
                elif dataConf.dataType == "BOOLEAN": 
                    value=BOOLEANGenerator(dataConf).getRandom()
                elif dataConf.dataType == "STRING":                     
                    value=STRINGGenerator(dataConf).getRandom(self.stringChoice[column.get('name')])
                elif dataConf.dataType == "TIMESTAMP":
                    value=timeStamp 
                elif dataConf.dataType == "NULL":
                    value=None  
                else: 
                    value=None                    
                #Process column information
                record.append(value) 
        except:
            #TO DO handle any error
            raise         
        return record
    
    def generateDataCount(self,count):  
        record=[]
        #To do for other records
        try:        
            for column in self.config.findall('column'):
                dataConf=RandomConfig(column)
                value= None
                if dataConf.dataType == "INTEGER":  
                    if dataConf.pattern == "Sequence":
                        value=IntegerGenrator(dataConf).getRandom(count)
                    else:
                        value=IntegerGenrator(dataConf).getRandom()
                elif dataConf.dataType == "FLOAT":
                    value=FloatGenrator(dataConf).getRandom()
                elif dataConf.dataType == "DECIMAL":
                    value=DecimalGenrator(dataConf).getRandom()
                elif dataConf.dataType == "GUID":
                    value=GUIDGenerator(dataConf).getRandom()
                elif dataConf.dataType == "ORDINAL": 
                    value=ORDINALGenerator(dataConf).getRandom(self.ordinalChoice[column.get('name')],self.odinalBias[column.get('name')])
                elif dataConf.dataType == "BOOLEAN": 
                    value=BOOLEANGenerator(dataConf).getRandom()
                elif dataConf.dataType == "STRING":                     
                    value=STRINGGenerator(dataConf).getRandom(self.stringChoice[column.get('name')])
                elif dataConf.dataType == "TIMESTAMP":
                    value=None 
                elif dataConf.dataType == "NULL":
                    value=None  
                else: 
                    value=None                    
                #Process column information
                record.append(value) 
        except:
            #TO DO handle any error
            raise         
        return record
 
    
 
    def loadStringChoice(self):
        choicedict={}
        for column in self.config.findall('column'):
            if "STRING" == column.findtext('datatype',default=None):  
                choice=column.find('choice')
                if choice is None:
                    choicedict[column.get('name')] = string.digits+string.uppercase+string.lowercase            
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
                    choicedict[column.get('name')]=s
        return choicedict
    
    def loadOrdinalChoice(self):
        choicedict={}
        bias_dict={}   
        for column in self.config.findall('column'):              
            if "ORDINAL" == column.findtext('datatype',default=None):  
                options=[]
                bias_list=[]
                choice=column.find('choice')
                seed=choice.get('seed',default=None)
                if seed is not None:
                    columnNO=choice.get('column',default=None)
                    if columnNO is None:
                        with open(seed) as f:
                            options=f.read().splitlines() 
                    else:  
                        options=self.loadSelectedColumn(seed, columnNO)
                else:
                    for opt in choice.findall('option'):
                        options.append(opt.text)        
                choicedict[column.get('name')]= options 
                optionsCount=len(options)
                choiceBias=choice.get('bias',default=None)
                if choiceBias is None:
                    for opt in choice.findall('option'):
                        if opt.get('bias',default=None) is None:                            
                            bias_list.append(1.0/optionsCount)
                        else:
                            bias_list.append(float(opt.get('bias',default=None)))
                else:
                    bias_string=choice.get('bias').split(',') 
                    uniformCount=optionsCount
                    remainingProbability=1.0
                    bias_choices={}
                    for s in bias_string:
                        v=s.split(':') 
                        if len(v)>1:
                            bias_choices[v[0]]=float(v[1])
                            remainingProbability-=float(v[1])                                          
                    for option in options:
                        if option in bias_choices:
                            bias_list.append(bias_choices[option])
                        else:
                            bias_list.append(remainingProbability/uniformCount) 
                scale=[]                
                for i in range(optionsCount):
                    s=0
                    for j in range(i+1):
                        s+=bias_list[j]
                    scale.append(s)
                scale[-1]=1.01                
                bias_dict[column.get('name')]=scale     
        return choicedict,bias_dict  

    def loadSelectedColumn(self,seed,column):
        columnNo=int(column)-1                                
        options=[]         
        try:
            with open(seed, 'rb') as f:
                reader = csv.reader(f, delimiter=',')                
                for row in reader:                    
                    options.append(row[columnNo])                                  
        except csv.Error as e:
            print "Seed file not found"
            raise e
        options=list(set(options[1:]))       
        return options 