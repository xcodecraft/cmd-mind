#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging
from impl.input_mode import *
from impl.receiver   import *


_logger = logging.getLogger()



class ModeTC(unittest.TestCase):
    def test_quote(self) :
        receiver = input_receiver()
        cur_mode = quote_mode(end_mode())
        line = """ abcd"aaa  """
        for c in line :
            cur_mode = cur_mode.mode(c)
            if cur_mode is not end_mode :
                cur_mode.input(c,receiver)
        
        self.assertEqual(receiver.data," abcd")
    def exec_mode(self,cur_mode,line,receiver) :
        for c in line :
            cur_mode = cur_mode.mode(c)
            if cur_mode is not end_mode :
                cur_mode.input(c,receiver)
    def test_prompt(self):
        pass
        receiver = input_receiver()
        cur_mode = prompt_mode(end_mode())
        line   =  "c\t"
#        self.exec_mode(cur_mode,line,receiver)
#        self.assertEqual(receiver.data,"conf")
        pass
    def test_all(self) :
        receiver = input_receiver()
        cur_mode = cmd_mode()
        line = """rg conf -s api -e dev"""
        self.exec_mode(cur_mode,line,receiver)
        self.assertEqual(receiver.data,line)

        #line = """rg conf -s api -e dev"""
        #self.exec_mode(cur_mode,line,receiver)
        #self.assertEqual(receiver.data,line)
