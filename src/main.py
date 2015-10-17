'''
Created on Aug 30, 2015

@author: Subhasis
'''
import sys
from datetime import datetime
from datasimu.service.DataGenerator import DataGenerator

if __name__ == '__main__':    
    print str(datetime.now())
    inputConfigurationFile=sys.argv[1]
    dataGenObj=DataGenerator(inputConfigurationFile)  
              
    processCompleate=dataGenObj.process()
    if processCompleate:
        print "DONE"
    else:
        print "NOT FINISHED."
    print str(datetime.now())