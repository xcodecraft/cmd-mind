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
    input_buf = [] 
    def get_char(self) :
        if len(self.input_buf ) <= 0 :
            ch = sys.stdin.read(1)
        else :
            ch = self.input_buf[0] 
            self.input_buf = self.input_buf[1:] 



        _logger.debug(",char:[%s : %s]" %(ch,binascii.b2a_hex(ch)))
        return ch
    def input_begin(self):
        self.cur_mode  = cmd_mode()
        self.recorder  = input_receiver()
        self.receiver = combin_receiver(self.recorder,console_receiver())
        pass
    def reback_begin(self):
        self.input_buf = self.recorder.data 
        self.receiver.reback_word(self.recorder.data)


    def input(self,cmder,node_iter) :
        self.input_begin() 
        cmd_prompt_mode.prompt_finder = lambda x,y : prompt_finder(self.recorder, node_iter).cmd_get(y)
        key_prompt_mode.prompt_finder = lambda x,y : prompt_finder(self.recorder, node_iter).key_get(y)
        val_prompt_mode.prompt_finder = lambda x,y : prompt_finder(self.recorder, node_iter).val_get(y)


        backing = False 
        print(node_iter.current.help())
        with  console_mode() :
            while True:
                    ch = self.get_char()
                    if ch == '\r' :
                        cmder.reset()
                        cmd_parser.parse(self.recorder.data,cmder)
                        _logger.info("receive cmd: %s" %(self.recorder.data))
                        break
                    if ch == DEL :
                        self.receiver.reback_char()
                        backing = True
                        continue 
                    else :
                        if backing  : 
                            backing        = False
                            self.reback_begin()
                            self.input_begin()
                            self.input_buf  += ch
                            continue 
                    self.cur_mode = self.cur_mode.mode(ch)
                    if self.cur_mode is not end_mode :
                        self.cur_mode.input(ch,self.receiver)
        return
