#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging
from impl.input_mode import *
from impl.receiver   import *
import utls.prompt 


_logger = logging.getLogger()


def test_prompter(values,key="") :
    return utls.prompt.iter(values,key, lambda x: x ) 

def exec_mode(cur_mode,line,receiver) :
    for c in line :
        cur_mode = cur_mode.mode(c)
        if cur_mode is not end_mode :
            cur_mode.input(c,receiver)

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
    def test_prompt(self):
        options           = ['conf', 'console', 'start','stop']
        receiver          = input_receiver()
        cur_mode          = prompt_mode(end_mode())
        cur_mode.prompter = lambda x : test_prompter(options,x)
        line              = "\t"
        exec_mode(cur_mode,line,receiver)
        self.assertEqual(receiver.data,"conf")
        line              = "\t"
        exec_mode(cur_mode,line,receiver)
        self.assertEqual(receiver.data,"console")

        line              = "\t\t"
        exec_mode(cur_mode,line,receiver)
        self.assertEqual(receiver.data,"stop")


    def test_prompt2(self):
        options           = ['conf', 'console', 'start','stop']
        receiver          = input_receiver()
        cur_mode          = prompt_mode(end_mode(),"c")
        cur_mode.prompter = lambda x : test_prompter(options,x)
        line              = "\t\t"
        exec_mode(cur_mode,line,receiver)
        self.assertEqual(receiver.data,"onsole")
        # line              = "\t"
        # exec_mode(cur_mode,line,receiver)
        # self.assertEqual(receiver.data,"onsole")

    def test_all(self) :
        receiver = input_receiver()
        cur_mode = cmd_mode()
        line = """rg conf -s api -e dev"""
        exec_mode(cur_mode,line,receiver)
        self.assertEqual(receiver.data,line)

        receiver = input_receiver()
        line = """rg conf -s 'api -e'  -e dev"""
        exec_mode(cur_mode,line,receiver)
        self.assertEqual(receiver.data,line)

        #TODO:

        # receiver = input_receiver()
        # line = """rg c\t -s api  -e dev"""
        # exec_mode(cur_mode,line,receiver)
        # self.assertEqual(receiver.data,line)
