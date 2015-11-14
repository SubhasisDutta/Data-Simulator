'''
Created on Nov 13, 2015

@author: Subhasis
'''
import datetime
from datasimu.generator.RecordGenerator import RecordGenerator

class UniformService(object):
    '''
    classdocs
    '''


    def __init__(self, manager,config):
        '''
        Constructor
        '''
        self.manager=manager
        self.config=config
        self.generator=RecordGenerator(self.config)
        
    def process(self):
        startTime=datetime.datetime.strptime(self.config.find('startindex').text, "%Y-%m-%dT%H:%M:%S")
        endTime=datetime.datetime.strptime(self.config.find('endindex').text, "%Y-%m-%dT%H:%M:%S")
        timeIterator=startTime
            
        while timeIterator < endTime:                 
            self.manager.push(self.generator.generateData(timeIterator))         
            timeIterator += self.getTimeDelta() 
    
    def getTimeDelta(self):
        timeDelta=self.config.find('timedelta').text
        timedeltaunit=self.config.find('timedeltaunit').text
        #microseconds, milliseconds, seconds, minutes, hours, days, weeks
        if timedeltaunit == 'seconds':
            return datetime.timedelta(seconds=int(timeDelta))
        if timedeltaunit == 'milliseconds':
            return datetime.timedelta(milliseconds=int(timeDelta))
        if timedeltaunit == 'minutes':
            return datetime.timedelta(minutes=int(timeDelta))
        if timedeltaunit == 'hours':
            return datetime.timedelta(hours=int(timeDelta))
        if timedeltaunit == 'days':
            return datetime.timedelta(days=int(timeDelta))
        if timedeltaunit == 'weeks':
            return datetime.timedelta(weeks=int(timeDelta)) 
        return datetime.timedelta(seconds=int(timeDelta))