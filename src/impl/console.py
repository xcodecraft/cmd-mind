#coding=utf-8
import sys,tty,termios
import binascii
import cmd_parser,calls
import pdb
import logging
from io_status import *
from input_mode import *
from impl.input_mode import *
from impl.receiver   import *
from impl.conf_yaml  import *
from impl.prompt     import *
# import utls.prompt 
import impl.input_mode  
# import impl.conf_iter 



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
        #tty.setcbreak(sys.stdin.fileno())
    def __exit__(self,exc_type,exc_value,traceback) :
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.settings)


class cmd_io :
    def get_char(self) :
        ch = sys.stdin.read(1)
        _logger.debug(",char:[%s : %s]" %(ch,binascii.b2a_hex(ch)))
        return ch

    def input(self,cmder,node_iter) :
        cur_mode = cmd_mode()
        recorder = input_receiver()
        receiver = combin_receiver(recorder,console_receiver())
        impl.input_mode._prompt_finder = lambda x,y : prompt_finder(recorder, node_iter).get(x,y)

        with  console_mode() :
            while True:
                    ch = self.get_char()
                    if ch == '\r' :
                        cmder.reset()
                        cmd_parser.parse(recorder.data,cmder)
                        break
                    if ch == DEL :
                        receiver.reback_char()

                    cur_mode = cur_mode.mode(ch)
                    if cur_mode is not end_mode :
                        cur_mode.input(ch,receiver)
        return  
