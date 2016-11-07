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
    for i in range(char_len) :
        sys.stdout.write(BS)
        sys.stdout.write(DEL)
        sys.stdout.write(BS)



class input_receiver :
    data         = ""
    input_word   = ""
    def record_char(self,ch) :
        sys.stdout.write(ch)
        self.data =  self.data + ch

    def record_word(self,word) :
        for c in word:
            self.record_char(c)

    def reback_char(self) :
        back_clear(1)
        self.data = self.data[0:-1]

    def reback_word(self,word) :
        for c in word:
            self.reback_char()
