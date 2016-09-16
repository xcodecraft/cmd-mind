#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging

from impl.conf_yaml import *
from impl.conf_iter import *
import define,xcmd,calls
class CallsTC(unittest.TestCase):
    def test_call(self) :
        calls.write_history("test","all")
        calls.write_history("test","patch")
        lines= calls.read_history("test")
        # self.assertTrue(iter.current.name , "console-ng")
        # self.assertEqual(iter.list_subs(),["all","patch"])
        # self.assertTrue(iter.next("all"))
        # self.assertTrue(not iter.next("all"))
        #
        # self.assertEqual(iter.list_args(),["prj","env","host"])
        # self.assertTrue(iter.match_cmds(cmder))
        # self.assertTrue(iter.match_args(cmder))

        self.assertTrue(True)
