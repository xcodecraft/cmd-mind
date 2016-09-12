#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging
import impl.console
class ConfTC(unittest.TestCase):
    def test_io(self) :
       impl.console.run() 
        self.assertTrue(True)
