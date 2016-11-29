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
        _logger.debug("init mode :%s" %(self.__class__.__name__))
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
            _logger.debug("back mode :%s" %(self.hismode.__class__.__name__))
            return self.hismode
        return self
    def _input(self,ch,receiver) :
        if not ch == '"' :
            receiver.record_char(ch)

class argkey_mode (input_mode):
    hot = True
    def mode(self,ch) :
        if ch == '-' :
            self.hot = False
        if ch == '\t' :
            word = self.receiver.data.strip().strip('-')
            return   key_prompt_mode(self,word,self.hot)
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
        word = self.receiver.data.strip().strip('=')
        _logger.debug("argval  word : %s" %(word))
        if ch == '\t' :
            return   val_prompt_mode(self,word, self.argkey)
        if ch == '"' :
            return quote_mode(self)
        if ch == ' ' :
            if len(word) > 0 :
                return space_mode()
        return self
    def _input(self,ch,receiver) :
        receiver.record_char(ch)



class prompt_mode (input_mode):
    def __init__(self,hismode,word=""):
        input_mode.__init__(self)
        self.hismode      = hismode
        self.last_prompt  = ""
        self.prompt_block = ""
        self.word         = word
        self.options      = None
        mode              = hismode.__class__.__name__
        clsname           = self.__class__.__name__
        _logger.debug("init %s prompter by %s " %(clsname,mode))

    def back(self,ch) :
        hismode = self.hismode.__class__.__name__
        self.hismode.receiver.data += self.receiver.data
        mode = self.hismode.mode(ch)
        _logger.debug("back mode:%s --> %s" %(hismode,mode.__class__.__name__))
        return mode
    def mode(self,ch) :
        if ch  == '=' :
            return self.back(ch)
        if ch  == ' ' :
            return self.back(ch)
            #return space_mode()
        return self
    def get_options(self):
        if self.options is None :
            self.options = self.prompter(self.word)
            _logger.debug("get prompter options by %s " %(self.word))
        return  self.options is not None
    def _input(self,ch,receiver) :
        if ch == '\t' :
            if self.prompter is not None :
                if not self.get_options() :
                    return
                last_prompt   = self.prompt_block
                try :
                    self.prompt_block= self.options.next().strip()
                    receiver.reback_word(last_prompt)
                    receiver.record_word(self.prompt_block)
                    _logger.info(" prompt :%s" %(self.prompt_block))
                except StopIteration :
                    _logger.debug(" none prompt " )
                    self.options = None
                    pass


class key_prompt_mode(prompt_mode) :
    prompt_finder = None
    def __init__(self,hismode,word="",  hot=True):
        prompt_mode.__init__(self,hismode,word)
        self.hot  = hot
        self.prompter     = self.prompt_finder("")
    def get_options(self):
        if self.options is None :
            self.options = self.prompter(self.word,self.hot)
            _logger.debug("get prompter options by %s hot:%s " %(self.word,self.hot))
        return  self.options is not None

class val_prompt_mode(prompt_mode):
    prompt_finder = None
    def __init__(self,hismode,word="",key="") :
        prompt_mode.__init__(self,hismode,word)
        self.prompter     = self.prompt_finder(key)
        _logger.debug("get prompter key %s " %(key))

class cmd_prompt_mode(prompt_mode) :
    prompt_finder = None
    def __init__(self,hismode,word=""):
        prompt_mode.__init__(self,hismode,word)
        self.prompter     = self.prompt_finder("")

class cmd_mode (input_mode):

    def mode(self,ch) :
        if ch == '\t' :
            return   cmd_prompt_mode(self,self.receiver.data)
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
