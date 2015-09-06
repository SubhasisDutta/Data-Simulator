'''
Created on Aug 30, 2015

@author: Subhasis
'''
import os
from com.dgstool.common.DataGenerator import DataGenerator

if __name__ == '__main__':
    #This file name needs to be changed based on the configuration required for the input data.
    inputConfigurationFile=os.path.join(os.path.dirname(__file__), "..\\config\\testconfig.xml")    
    dataGenObj=DataGenerator(inputConfigurationFile)       
    processCompleate=dataGenObj.process()
    if processCompleate:
        print "DONE"
    else:
        print "NOT FINISHED."