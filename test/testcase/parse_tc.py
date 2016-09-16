#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging

import impl.cmd_parser 
import xcmd
class parse_tc(unittest.TestCase):

    def test_cmd(self):
        input = "test all "
        cmder = xcmd.commander 
        impl.cmd_parser.parse(input,cmder)
        self.assertEqual(cmder.cmds,["test","all"])
        
        
    def test_arg(self):
        input = "-p pylon"
        cmder = xcmd.commander 
        impl.cmd_parser.parse(input,cmder)
        self.assertEqual(cmder.args,{"p":"pylon"})

        args = impl.cmd_parser.parse_args(input)
        self.assertEqual(args,{"p":"pylon"})
        
    def test_arg(self):
        input = "--prj=pylon"
        cmder = xcmd.commander 
        impl.cmd_parser.parse(input,cmder)
        self.assertEqual(cmder.args,{"prj":"pylon"})

        args = impl.cmd_parser.parse_args(input)
        self.assertEqual(args,{"prj":"pylon"})
        
        
    def test_arg_bad(self):
        input = "-p "
        cmder = xcmd.commander 
        impl.cmd_parser.parse(input,cmder)
        self.assertEqual(cmder.args,{})
        
        args = impl.cmd_parser.parse_args(input)
        self.assertEqual(args,{"p" : None})
        
    def test_arg_bad2(self):
        input = "-p=1 "
        cmder = xcmd.commander 
        impl.cmd_parser.parse(input,cmder)
        self.assertEqual(cmder.args,{})
        
        args = impl.cmd_parser.parse_args(input)
        
    def test_arg_bad3(self):
        input = "-p=1 pylon"
        cmder = xcmd.commander 
        impl.cmd_parser.parse(input,cmder)
        #self.assertEqual(data['args'],{})
        
        args = impl.cmd_parser.parse_args(input)
        #self.assertEqual(args,{})
        

    def test_arg_short(self):
        input = "test all -p pylon -e dev"
        cmder = xcmd.commander 
        impl.cmd_parser.parse(input,cmder)
        self.assertEqual(cmder.cmds,["test","all"])
        self.assertEqual(cmder.args,{"p":"pylon", "e":"dev"})

    def test_arg_short2(self):
        cmder = xcmd.commander 
        input = """test all -p "pylon = 1" -e dev"""
        impl.cmd_parser.parse(input,cmder)
        self.assertEqual(cmder.cmds,["test","all"])
        self.assertEqual(cmder.args,{"p":"pylon = 1", "e":"dev"})

    def test_arg_long(self):
        cmder = xcmd.commander 
        input = "test all --prj=pylon --env=dev"
        impl.cmd_parser.parse(input,cmder)
        self.assertEqual(cmder.cmds,["test","all"])
        self.assertEqual(cmder.args,{"prj":"pylon", "env":"dev"})
