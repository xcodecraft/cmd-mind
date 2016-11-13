#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging
from impl.input_mode import *
from impl.receiver   import *
from impl.conf_yaml  import *
from impl.prompt     import *
from tc_utls  import *
import utls.prompt
import impl.conf_iter


_logger = logging.getLogger("tc")


def test_prompter(key="") :
    values  = ['conf', 'console', 'start','stop']
    return utls.prompt.iter(values,key, lambda x: x )

def exec_mode(cur_mode,line,receiver) :
    last_mode = None
    for c in line :
        _logger.debug("input: '%s'" %c)
        # last_mode = cur_mode
        cur_mode  = cur_mode.mode(c)
        # if isinstance(last_mode,prompt_mode) :
        #     cur_mode  = cur_mode.mode(c)
        #     break
            # else:
                # print( "last: %s,cur: %s" %(last_mode.__class__.__name__, cur_mode.__class__.__name__))
        if cur_mode is not end_mode :
            cur_mode.input(c,receiver)


class ModeTC(unittest.TestCase,Log4TC):
    def setUp(self) :
        cmd_prompt_mode.prompt_finder =  lambda x,y : test_prompter
        key_prompt_mode.prompt_finder =  lambda x,y : test_prompter
        val_prompt_mode.prompt_finder =  lambda x,y : test_prompter

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
        receiver          = input_receiver()
        cur_mode          = cmd_prompt_mode(end_mode())
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
        receiver          = input_receiver()
        cur_mode          = cmd_prompt_mode(end_mode(),"c")
        line              = "\t\t"
        exec_mode(cur_mode,line,receiver)
        self.assertEqual(receiver.data,"onsole")
        # line              = "\t"
        # exec_mode(cur_mode,line,receiver)
        # self.assertEqual(receiver.data,"onsole")

class AllModeTC(unittest.TestCase,Log4TC):
    def setUp(self) :
        Log4TC.setUp(self)
        testRoot  = os.path.dirname(os.path.realpath(__file__))
        testRoot  = os.path.dirname(testRoot)
        self.data = load_conf(testRoot + "/data/rg.yml","!","define.")

    def mode_do(self,line,receiver) :
        iter          = impl.conf_iter.node_iter(self.data)
        cmd_prompt_mode.prompt_finder = lambda x,y : prompt_finder(receiver, iter ).cmd_get(y)
        key_prompt_mode.prompt_finder = lambda x,y : prompt_finder(receiver, iter ).key_get(y)
        val_prompt_mode.prompt_finder = lambda x,y : prompt_finder(receiver, iter ).val_get(y)
        cur_mode = cmd_mode()
        exec_mode(cur_mode,line,receiver)

    def test_1(self) :

        receiver = input_receiver()
        line     = """rg conf -s api -e dev"""
        self.mode_do(line,receiver)
        self.assertEqual(receiver.data,line)
        return

    def test_2(self) :
        receiver = input_receiver()
        line     = """rg conf -s 'api -e'  -e dev"""
        self.mode_do(line,receiver)
        self.assertEqual(receiver.data,line)

    def test_3(self) :

        receiver = input_receiver()
        line = """rg c\t -s api -e dev"""
        self.mode_do(line,receiver)
        self.assertEqual(receiver.data,"rg conf -s api -e dev")

    def test_4(self) :
        receiver = input_receiver()
        line = """rg c\t --sys=a\t --env= \t"""
        self.mode_do(line,receiver)
        self.assertEqual(receiver.data,"rg conf --sys=api --env= dev")

    def test_5(self) :
        receiver = input_receiver()
        line = """rg c\t\t --sys \t --env \t"""
        self.mode_do(line,receiver)
        self.assertEqual(receiver.data,"rg conf,stop --sys api --env dev")

        receiver = input_receiver()
        line = """rg c\t\t -s \t --env \t"""
        self.mode_do(line,receiver)
        self.assertEqual(receiver.data,"rg conf,stop -s api --env dev")

    def test_6(self) :
        receiver = input_receiver()
        line = """rg c\t\t --s\t \t --env \t"""
        self.mode_do(line,receiver)
        self.assertEqual(receiver.data,"rg conf,stop --sys api --env dev")

        # receiver = input_receiver()
        # line = """rg c\t\t -s \t --env \t"""
        # self.mode_do(line,receiver)
        # self.assertEqual(receiver.data,"rg conf,stop -s api --env dev")

    def test_7(self) :
        receiver = input_receiver()
        line = """rg c\t\t --sys \t\t --env \t"""
        self.mode_do(line,receiver)
        self.assertEqual(receiver.data,"rg conf,stop --sys web --env dev")
