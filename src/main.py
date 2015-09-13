'''
Created on Aug 30, 2015

@author: Subhasis
'''
import sys
from datasimu.service.DataGenerator import DataGenerator

if __name__ == '__main__':    
    inputConfigurationFile=sys.argv[1]
    dataGenObj=DataGenerator(inputConfigurationFile)       
    processCompleate=dataGenObj.process()
    if processCompleate:
        print "DONE"
    else:
        print "NOT FINISHED."