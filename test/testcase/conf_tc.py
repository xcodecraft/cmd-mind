#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging

from impl.conf_yaml import *
from impl.conf_iter import *
import define,xcmd
class ConfTC(unittest.TestCase):
    def test_load(self) :
        testRoot = os.path.dirname(os.path.realpath(__file__))
        testRoot = os.path.dirname(testRoot)

        data = load_conf(testRoot + "/data/conf.yml","!","define.")

        cmder = xcmd.commander("test")
        cmder.cmds=["console-ng","all"] 
        cmder.args={"prj":"pylon", "env" : "dev", "host" : "127.0.0.1"}
        iter  = node_iter(data)
        self.assertTrue(iter.current.name , "console-ng")
        self.assertTrue(iter.next("all"))
        self.assertTrue(not iter.next("all"))

        iter.walk(["console-ng" , "all"])
        self.assertEqual(iter.current.name , "all")
        iter.walk(["console-ng" , "al2"])
        self.assertEqual(iter.current.name , "console-ng")
