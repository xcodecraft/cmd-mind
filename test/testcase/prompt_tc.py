#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging
from impl.prompt import *
from impl.conf_iter import * 
from impl.conf_yaml import *
from impl.receiver import *
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
        options = iter.current.get_prompter("") 

        what = ""
        what    = options.next()
        self.assertEqual(what,"conf")
        what    = options.next()
        self.assertEqual(what,"start")
        what    = options.next()
        self.assertEqual(what,"stop")

        iter.walk(cmder.cmds)
        options = iter.current.get_prompter("s") 
        what    = options.next()
        self.assertEqual(what,"tart")
        what    = options.next()
        self.assertEqual(what,"top")

        options = iter.get_prompter()
        self.assertEqual(options,None)

        options = iter.current.args_prompter()
        what     = options.next()
        self.assertEqual(what,"env")

        what     = options.next()
        self.assertEqual(what,"sys")

        options = iter.current.args_prompter(hot=True)
        what     = options.next()
        self.assertEqual(what,"e")

        what     = options.next()
        self.assertEqual(what,"s")

        options = iter.current.get_arg('env').value_prompter()
        what     = options.next()
        self.assertEqual(what,"dev")

        what     = options.next()
        self.assertEqual(what,"lab")

        what     = options.next()
        self.assertEqual(what,"demo")

        # try :
        #     what    = options.next()
        #     self.assertTrue(False)
        # except StopIteration  as e :
        #     self.assertTrue(True)
        #
        # options = iter.current.args_prompter("s") 

    def test_finder(self) :
        testRoot      = os.path.dirname(os.path.realpath(__file__))
        testRoot      = os.path.dirname(testRoot)
        data          = load_conf(testRoot + "/data/rg.yml","!","define.")
        iter          = node_iter(data)
        receiver      = input_receiver()
        finder        = prompt_finder(receiver, iter )

        receiver.data = "c"
        prompter      = finder.get("cmd_mode")
        options       = prompter("c")
        what          = options.next()
        self.assertEqual(what,"onf")

        what          = options.next()
        self.assertEqual(what,"onf,stop")

        receiver.data = "conf --"
        prompter      = finder.get("argkey_mode")
        options       = prompter("")
        what          = options.next()
        self.assertEqual(what,"env")
        what          = options.next()
        self.assertEqual(what,"sys")


        receiver.data = "conf --"
        prompter      = finder.get("argkey_mode")
        options       = prompter("s")
        what          = options.next()
        self.assertEqual(what,"ys")


        receiver.data = "conf --env="
        prompter      = finder.get("argval_mode","env")
        options       = prompter("")
        what          = options.next()
        self.assertEqual(what,"dev")


