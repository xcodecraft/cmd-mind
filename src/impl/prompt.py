#coding=utf-8
import sys,tty,termios
import binascii
import cmd_parser,calls
import pdb
import logging

_logger = logging.getLogger()

class block_prompt :
    def bind(self,cmder,node_iter):
        self.cmder = cmder 
        self.node_iter = node_iter 

    def get_promptor(self) :
        prompt_iter = None
        if (not self.node_iter.match_cmds(self.cmder) ) and self.node_iter.have_subs() :
            prompt_iter = self.node_iter.next_sub(self.cmder)
            _logger.debug("cmd prompt")
        elif (not self.node_iter.match_args(self.cmder) ) and self.node_iter.have_args() :
            prompt_iter = self.node_iter.next_arg(self.cmder)
            _logger.debug("arg prompt")
        return prompt_iter

    def prompt(self,word) :
        name_iter = self.get_promptor()
        input_len = len(word)
        for data in name_iter :
            _logger.debug("block prompt option:%s" %(data))
            if word[0:input_len] ==  data[0:input_len] :
                p_word = data[input_len :]
                _logger.debug("prompt: %s" %p_word)
                yield p_word 
                _logger.debug("prompt: continue")
                #return p_word
        #yield None
        #return None


class value_prompt :
    def find_value_prompt(self,key,cmder,node_iter) :
        if self.value_iter is not None :
            return True
        for arg in node_iter.current.args :
            if arg.name == key :
                    self.value_iter  = arg.option_next()
                    return True
        return False
    def value_prompt(self,key,cmder,node_iter) :
        stop_count = 0
        while(True):
            try :
                self.prompt_value   = self.value_iter.next()
                _logger.debug("prompt: %s" %self.prompt_value)
                return True
            except StopIteration:
                self.value_iter = None
                if stop_count > 10 :
                    return False
                stop_count += 1
                if not self.find_value_prompt(key,cmder,node_iter) :
                    return False
