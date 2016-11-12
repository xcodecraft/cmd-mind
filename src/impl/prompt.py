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
    def get(self,mode,key=""):
        cmder    = xcmd.commander("")
        cmd_parser.parse(self.receiver.data,cmder)
        self.iter.walk(cmder.cmds)
        if mode == 'cmd_mode' :
            # 首先优先
            if len (self.iter.current.options ) >0 :
                return self.iter.current.get_prompter
            return self.iter.get_prompter
        if mode == 'argkey_mode' :
            return self.iter.current.args_prompter
        if mode == 'argval_mode' :
            arg = self.iter.current.get_arg(key)
            if arg == None :
                _logger.warning( "not found arg:%s in %s" %(key,self.iter.current.name))
                return None 
            return arg.value_prompter
        return  None 
    
