#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging
from impl.console_io  import *

def prompt_sutb(ins,prefix) :
    return "odecraft"

_logger = logging.getLogger()
class ConfTC(unittest.TestCase):
    def test_cmdio(self) :
        _logger.debug("in %s " %("test_cmdio"))
        cmd = cmd_io() 
        input = "hello boy\r"
        god   = io_god()
        for c in input :
            god.io(c)
        self.assertEqual(input.strip(),god.input)

        input = "hello" + DEL  + "\r"
        god   = io_god()
        for c in input :
            god.io(c)
        self.assertEqual("hell",god.input)
        cmd_io.prompter = prompt_sutb 
        input = "xc\t\r" 
        god   = io_god()
        for c in input :
            god.io(c)
        self.assertEqual("xcodecraft",god.input)

        input = "xcc" + DEL + "\t\r" 
        god   = io_god()
        for c in input :
            god.io(c)
        self.assertEqual("xcodecraft",god.input)

    def test_args(self) :
        _logger.debug("in %s " %("test_args"))
        input = "--key=hello\r"
        god   = io_god()
        for c in input :
            god.io(c)
        self.assertEqual(input.strip(),god.input)

        input = "-k hello\r"
        god   = io_god()
        for c in input :
            god.io(c)
        self.assertEqual(input.strip(),god.input)
