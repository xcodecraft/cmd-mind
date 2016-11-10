#coding=utf-8
import sys,tty,termios
import binascii
import cmd_parser,calls
import pdb
import logging

_logger = logging.getLogger()

class input_mode :
    def mode(self,ch) :
        pass
    def input(self,ch,receiver) :
        pass 


class end_mode:
    def mode(self,ch) :
        return self
    def input(self,ch,receiver) :
        pass 

class quote_mode:
    def __init__(self,hismode):
        self.hismode = hismode

    def mode(self,ch) :
        if ch == '"' :
            return self.hismode 
        return self 
    def input(self,ch,receiver) :
        if not ch == '"' :
            receiver.record_char(ch)

class argkey_mode:
    def mode(self,ch) :
        if ch == ' ' :
            return argval_mode() 
        if ch == '=' :
            return argval_mode() 
        return self 

    def input(self,ch,receiver) :
        if ch == '"' :
            return 
        receiver.record_char(ch)

class argval_mode :

    def mode(self,ch) :
        if ch == '"' :
            return quote_mode(self)
        return self 
    def input(self,ch,receiver) :
        if ch == '=' :
#            if self.find_value_prompt(arg_key) :
#                _logger.debug("found value promptor")
#                if self.value_prompt(arg_key) :
#                        receiver.record_word(self.prompt_value)
            pass
        receiver.record_char(ch)
        pass 

class prompt_mode:
    prompter  = None 
    def __init__(self,hismode,word=""):
        self.hismode      = hismode
        self.last_prompt  = ""
        self.prompt_block = ""
        self.word         = word
        self.options      = None

    def mode(self,ch) :
        if ch  == ' ' :
            return self.hismode 
        return self 
    def input(self,ch,receiver) :
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

class cmd_mode:
    cmd_prompter = None 
    def mode(self,ch) :
        if ch == '\t' :
            mode =  prompt_mode(self)
            mode.prompter = self.cmd_prompter 
            return  mode 
        if ch == '"' :
            return quote_mode(hismode=self) 
        if ch == '-' :
            return argkey_mode() 
        return self 

    def input(self,ch,receiver) :
        receiver.record_char(ch)
