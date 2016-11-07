#coding=utf-8
import sys,tty,termios
import binascii
import cmd_parser,calls
import pdb
import logging
from io_status import *
from input_mode import *

BS  = binascii.a2b_hex("08")
DEL = binascii.a2b_hex("7F")
ESC = binascii.a2b_hex("1B")
_logger = logging.getLogger()

def complement(cmder,node_iter):
    pio         = cmd_io()
    line        = pio.input( cmder,node_iter)

class console_mode :
    def __enter__(self) :
        self.fd = sys.stdin.fileno()
        self.settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin.fileno())
    def __exit__(self,exc_type,exc_value,traceback) :
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.settings)


class cmd_io :
    name_iter    = None
    value_iter   = None
    prompt_block  = ""
    prompt_value = ""
    input_line   = ""
    input_word   = ""
    input_status = []

    def __init__(self):
        pass

    def input_over(self,cmder,node_iter) :
        cmder.reset()
        cmd_parser.parse(self.input_line,cmder)
        node_iter.walk(cmder.cmds)


    def get_char(self) :
        ch = ''
        if len(self.auto_buffer) > 0 :
            ch = self.auto_buffer[0]
            self.auto_buffer = self.auto_buffer[1:]
        else :
            ch = sys.stdin.read(1)
        return ch


    def input(self,cmder,node_iter) :
        self.auto_buffer =  str(cmder)
        self.status      = io_status()
        self.status.to_unknow()
        input_mode      = cmd_mode()
        receiver = input_receiver() 
        with  console_mode() :
            while True:
                    ch = self.get_char()
                    _logger.debug(",char:%s" %(ch))
                    if ch == '\r' :
                        self.input_over(cmder,node_iter)
                    if ch == DEL :
                        receiver.reback_char()
                    input_mode = input_mode(ch)
                    input_mode.input(ch,cmder,node_iter)
                    return  self.receiver.data
