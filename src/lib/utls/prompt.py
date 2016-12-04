#coding=utf-8
import error
import os,string,logging
from  utls.logger import *

def iter(options,word,func):
    input_len = len(word)
    for obj in options :
        data = func(obj) 
        debug_log("option: %s, word:%s : obj:%s" %(data,word,obj.__class__.__name__),'prompter')
        if word[0:input_len] ==  data[0:input_len] :
            p_word = data[input_len :]
            debug_log("prompt: %s" %p_word, 'prompter')
            yield p_word 
