#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging
from impl.prompt import *
from impl.conf_iter import * 
from impl.conf_yaml import *
import impl.cmd_parser , xcmd



_logger = logging.getLogger()

class PromptTC(unittest.TestCase):
    def test_prompt(self) :

        testRoot = os.path.dirname(os.path.realpath(__file__))
        testRoot = os.path.dirname(testRoot)
        data = load_conf(testRoot + "/data/rg.yml","!","define.")

        cmd_line = "conf"
        cmder    = xcmd.commander("rg")
        impl.cmd_parser.parse(cmd_line,cmder)
        iter     = node_iter(data)
        iter.walk(cmder.cmds)
        promptor = iter.current.get_prompter("") 

        what = ""
        what    = promptor.next()
        self.assertEqual(what,"conf")
        what    = promptor.next()
        self.assertEqual(what,"start")
        what    = promptor.next()
        self.assertEqual(what,"stop")

        iter.walk(cmder.cmds)
        promptor = iter.current.get_prompter("s") 
        what    = promptor.next()
        self.assertEqual(what,"tart")
        what    = promptor.next()
        self.assertEqual(what,"top")

        promptor = iter.get_prompter()
        self.assertEqual(promptor,None)

        promptor = iter.current.args_prompter()
        what     = promptor.next()
        self.assertEqual(what,"env")

        what     = promptor.next()
        self.assertEqual(what,"sys")

        promptor = iter.current.args_prompter(hot=True)
        what     = promptor.next()
        self.assertEqual(what,"e")

        what     = promptor.next()
        self.assertEqual(what,"s")


        # try :
        #     what    = promptor.next()
        #     self.assertTrue(False)
        # except StopIteration  as e :
        #     self.assertTrue(True)
        #
        # promptor = iter.current.args_prompter("s") 

