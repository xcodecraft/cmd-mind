#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging

from impl.conf_yaml import *
import define
class ConfTC(unittest.TestCase):
    def test_load(self) :
        testRoot = os.path.dirname(os.path.realpath(__file__))
        testRoot = os.path.dirname(testRoot)

        data = load_conf(testRoot + "/data/conf.yml","!","define.")

        # data= data['console-ng']
        cmder = define.commander()
        iter  = define.node_iter(data,cmder)
        iter.list_next()
        iter.next("all")
        iter.list_next()
        iter.next("--prj = pylon")
        iter.list_next()
        iter.back()
        iter.list_next()
        iter.next("--env = dev")
        iter.back()
        iter.list_next()

        cmder.show()
        # print(data['console-ng'])

        self.assertTrue(True)
