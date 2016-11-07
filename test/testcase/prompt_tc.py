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

        cmd_line = "rg"
        cmder    = xcmd.commander("rg")
        impl.cmd_parser.parse(cmd_line,cmder)
        iter     = node_iter(data)
        prompt   = block_prompt()
        prompt.bind(cmder,iter)

        promptor = prompt.prompt("")
        what1,what2,what3,what4,what5 = "","","","",""
        what1    = promptor.next()
        what2    = promptor.next()
        #what3    = promptor.next()
        #what4    = promptor.next()
        #what5    = promptor.next()
        print("\nprompt:%s,%s,%s,%s,%s" %(what1,what2,what3,what4,what5))

        #what    = prompt.prompt("c")
        #self.assertEqual(what,"onf")
        #print("\n data: %s \n" %(what))
