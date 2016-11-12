#coding=utf-8
import sys,tty,termios
import binascii
import cmd_parser,calls
import pdb
import logging
from receiver  import *

_logger = logging.getLogger("mode")
_prompter = None 

class input_mode :
    def __init__(self) :
        _logger.debug("to :%s" %(self.__class__.__name__))
        self.receiver = input_receiver()
    def mode(self,ch) :
        pass
    def input(self,ch,receiver) :
        combin = combin_receiver(self.receiver,receiver)
        self._input(ch,combin)

    def _input(self,ch,receiver) :
        pass 

class end_mode (input_mode):
    def mode(self,ch) :
        return self 
    def input(self,ch,receiver) :
        pass

class space_mode (input_mode):
    def mode(self,ch) :
        if ch == '-' :
            return argkey_mode() 
        if ch == ' ' :
            return self 
        return cmd_mode() 

    def input(self,ch,receiver) :
        receiver.record_char(ch)

class quote_mode( input_mode ):
    def __init__(self,hismode):
        input_mode.__init__(self)
        self.hismode = hismode

    def mode(self,ch) :
        if ch == '"' :
            return self.hismode 
        return self 
    def _input(self,ch,receiver) :
        if not ch == '"' :
            receiver.record_char(ch)

class argkey_mode (input_mode):
    def mode(self,ch) :
        if ch == '\t' :
            return   prompt_mode(self,self.receiver.data)
        if ch == ' ' :
            key =  self.receiver.data.strip('-')
            return argval_mode(key ) 
        if ch == '=' :
            key =  self.receiver.data.strip('-')
            return argval_mode( key ) 
        return self 

    def _input(self,ch,receiver) :
        if ch == '"' :
            return 
        receiver.record_char(ch)

class argval_mode (input_mode) :

    def __init__(self,argkey) :
        input_mode.__init__(self) 
        self.argkey = argkey 
    def mode(self,ch) :
        if ch == '\t' :
            word = self.receiver.data.strip().strip('=')
            return   prompt_mode(self,word, key=self.argkey)
        if ch == '"' :
            return quote_mode(self)
        return self 
    def _input(self,ch,receiver) :
        receiver.record_char(ch)

_prompt_finder = None 
class prompt_mode (input_mode):
    prompter  = None 
    def __init__(self,hismode,word="", key=""):
        input_mode.__init__(self)
        self.hismode      = hismode
        self.last_prompt  = ""
        self.prompt_block = ""
        self.word         = word
        self.options      = None
        mode =  hismode.__class__.__name__ 
        _logger.debug("get _prompter by %s %s" %(mode,key))
        self.prompter     = _prompt_finder(self.hismode.__class__.__name__,key)


    def mode(self,ch) :
        if ch  == ' ' :
            # return self.hismode 
            return space_mode()
        return self 
    def _input(self,ch,receiver) :
        if ch == '\t' :
            if self.prompter is not None :
                if self.options is None :
                    self.options = self.prompter(self.word)
                last_prompt   = self.prompt_block
                try :
                    self.prompt_block= self.options.next()
                    receiver.reback_word(last_prompt)
                    receiver.record_word(self.prompt_block)
                    _logger.info(" prompt :%s" %(self.prompt_block))
                except StopIteration :
                    self.options = None 
                    pass


class cmd_mode (input_mode):
    def mode(self,ch) :
        if ch == '\t' :
            return   prompt_mode(self,self.receiver.data)
        if ch == '-' :
            return argkey_mode() 
        if ch == ' ' :
            return space_mode()
        return self 

    def _input(self,ch,receiver) :
        if ch == '\t' :
            return 
        if ch == '"' :
            return 
        if ch == '-' :
            return 
        receiver.record_char(ch)
