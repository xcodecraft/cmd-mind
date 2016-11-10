#coding=utf-8
import error
import os,string,logging
_logger = logging.getLogger()

def iter(options,word,func):
    input_len = len(word)
    for obj in options :
        data = func(obj) 
        _logger.debug("[prompt] option: %s, word:%s" %(data,word))
        if word[0:input_len] ==  data[0:input_len] :
            p_word = data[input_len :]
            _logger.debug("prompt: %s" %p_word)
            yield p_word 
