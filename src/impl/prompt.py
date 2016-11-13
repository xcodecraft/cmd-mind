#coding=utf-8
import sys,tty,termios
import binascii
import cmd_parser,calls
import logging
import pdb
import xcmd

_logger = logging.getLogger()

class prompt_finder :

    def __init__(self,receiver,iter):
        self.receiver = receiver
        self.iter   = iter
    def cmd_get(self,key=""):
        cmder    = xcmd.commander("")
        cmd_parser.parse(self.receiver.data,cmder)
        self.iter.walk(cmder.cmds)
        # 首先优先
        if len (self.iter.current.get_options() ) >0 :
            _logger.debug("use cmd options prompte")
            return self.iter.current.get_prompter
        return self.iter.get_prompter
    def key_get(self,key="") :
        cmder    = xcmd.commander("")
        cmd_parser.parse(self.receiver.data,cmder)
        self.iter.walk(cmder.cmds)
        _logger.debug("use args prompte")
        return self.iter.current.args_prompter

    def val_get(self,key=""):
        cmder    = xcmd.commander("")
        cmd_parser.parse(self.receiver.data,cmder)
        self.iter.walk(cmder.cmds)
        _logger.debug("use arg value prompte key: %s" %(key))
        arg = self.iter.current.get_arg(key)
        if arg == None :
            _logger.warning( "not found arg:%s in %s" %(key,self.iter.current.name))
            return None
        return arg.value_prompter

