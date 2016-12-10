#coding=utf-8
import sys,tty,termios
import binascii
import cmd_parser,calls
import pdb
import logging

BS  = binascii.a2b_hex("08")
DEL = binascii.a2b_hex("7F")
ESC = binascii.a2b_hex("1B")
_logger = logging.getLogger()

def back_clear(char_len) :
    _logger.debug("del %s" %(char_len))
    for i in range(char_len) :
        sys.stdout.write(BS)
        sys.stdout.write(binascii.a2b_hex("20"))
        sys.stdout.write(BS)


class combin_receiver:
    def __init__(self,first,second) :
        self.first = first 
        self.second = second 
        
    def record_char(self,ch) :
        self.first.record_char(ch)
        self.second.record_char(ch)

    def record_word(self,word) :
        self.first.record_word(word)
        self.second.record_word(word)

    def reback_char(self) :
        self.first.reback_char()
        self.second.reback_char()

    def reback_word(self,word) :
        self.first.reback_word(word)
        self.second.reback_word(word)
    

class input_receiver :
    data         = ""
    input_word   = ""
    def record_char(self,ch) :
        self.data =  self.data + ch

    def record_word(self,word) :
        for c in word:
            self.record_char(c)

    def reback_char(self) :
        self.data = self.data[0:-1]

    def reback_word(self,word) :
        for c in word:
            self.reback_char()

class console_receiver :
    input_word   = ""
    def record_char(self,ch) :
        sys.stdout.write(ch)

    def record_word(self,word) :
        for c in word:
            self.record_char(c)

    def reback_char(self) :
        back_clear(1)

    def reback_word(self,word) :
        for c in word:
            self.reback_char()
