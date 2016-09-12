#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging

import impl.cmd_parser 
class parse_tc(unittest.TestCase):

    def test_cmd(self):
        input = "test all "
        data = impl.cmd_parser.parse(input)
        self.assertEqual(data['cmds'],["test","all"])
        
        
    def test_arg(self):
        input = "-p pylon"
        data = impl.cmd_parser.parse(input)
        self.assertEqual(data['args'],{"p":"pylon"})
        
    def test_arg_bad(self):
        input = "-p "
        data = impl.cmd_parser.parse(input)
        self.assertEqual(data['args'],{})
        
    def test_arg_bad2(self):
        input = "-p=1 "
        data = impl.cmd_parser.parse(input)
        self.assertEqual(data['args'],{})
        
    def test_arg_bad3(self):
        input = "-p=1 pylon"
        data = impl.cmd_parser.parse(input)
        #self.assertEqual(data['args'],{})
        

    def test_arg_short(self):
        input = "test all -p pylon -e dev"
        data = impl.cmd_parser.parse(input)
        self.assertEqual(data['cmds'],["test","all"])
        self.assertEqual(data['args'],{"p":"pylon", "e":"dev"})

    def test_arg_short2(self):
        input = """test all -p "pylon = 1" -e dev"""
        data = impl.cmd_parser.parse(input)
        self.assertEqual(data['cmds'],["test","all"])
        self.assertEqual(data['args'],{"p":"pylon = 1", "e":"dev"})

    def test_arg_long(self):
        input = "test all --prj=pylon --env=dev"
        data = impl.cmd_parser.parse(input)
        self.assertEqual(data['cmds'],["test","all"])
        self.assertEqual(data['args'],{"prj":"pylon", "env":"dev"})