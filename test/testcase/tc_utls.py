#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging

def logging_begin(tc,method):
    logger = logging.getLogger("tc")
    logger.info( "---------TC:%s method:%s--------" %(tc.__class__.__name__,method))

def logging_end(tc,method):
    logger = logging.getLogger("tc")
    logger.info( "===========TC:%s method:%s==========" %(tc.__class__.__name__,method))

class Log4TC :
    def setUp(self) :
        logging_begin(self,self._testMethodName)

    def tearDown(self):
        logging_end(self,self._testMethodName)

