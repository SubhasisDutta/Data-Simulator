'''
Created on Sep 23, 2015

@author: Subhasis
'''

class TweetService(object):
    '''
    This will generate Tweets based on seed Author and tweets and push data to storege of choice.
    '''

    def __init__(self, manager,config):
        '''
        Constructor
        '''
        self.manager=manager
        self.config=config
        
    def process(self):
        pass