#coding=utf-8
import sys,tty,termios
import binascii
import cmd_parser
import pdb
import logging


BS  = binascii.a2b_hex("08")
DEL = binascii.a2b_hex("7F")
ESC = binascii.a2b_hex("1B")
_logger = logging.getLogger()

def complement(cmder,node_iter):
    pio         = prompt_io()
    line        = pio.input_line( cmder,node_iter)

class console_mode :
    def __enter__(self) :
        self.fd = sys.stdin.fileno()
        self.settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin.fileno())
    def __exit__(self,exc_type,exc_value,traceback) :
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.settings)

def back_clear(char_len) :
    for i in range(char_len) :
        sys.stdout.write(BS)
        sys.stdout.write(DEL)
        sys.stdout.write(BS)

class prompt_io :
    name_iter  = None
    value_iter = None
    prompt_name = ""
    prompt_value = ""
    input_line  = ""
    input_word  = ""

    def get_promptor(self,cmder,node_iter) :
        prompt_iter = None
        if (not node_iter.match_cmds(cmder) ) and node_iter.have_subs() :
            prompt_iter = node_iter.next_sub()

        if (not node_iter.match_args(cmder) ) and node_iter.have_args() :
            prompt_iter = node_iter.next_arg(cmder.args)
        return prompt_iter
    def find_name_prompt(self,cmder,node_iter) :
        #pdb.set_trace()
        if self.name_iter is None :
            self.name_iter = self.get_promptor(cmder,node_iter)
            return self.name_iter is not None
        return  True

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
            except :
                self.value_iter = None
                if stop_count > 10 :
                    return False
                stop_count += 1
                if not self.find_value_prompt(key,cmder,node_iter) :
                    return False


    def name_prompt(self,word,cmder,node_iter) :
        stop_count = 0
        while(True):
            try :
                data      = self.name_iter.next()
                input_len = len(word.strip())
                if word[0:input_len] ==  data[0:input_len] :
                    p_word = data[input_len :]
                    self.prompt_name = p_word
                    _logger.debug("prompt: %s" %self.prompt_name)
                    return True
            except :
                self.name_iter = None
                if stop_count > 10 :
                    return False
                stop_count += 1
                if not self.find_name_prompt(cmder,node_iter) :
                    return False


    def clean_prompt(self):
        self.name_iter      = None
        self.value_iter     = None
        self.prompt_name    = ""
        self.prompt_value   = ""

    def input_over(self,cmder,node_iter) :
        self.input_line = self.input_line + self.input_word
        self.input_word = ""
        cmder.reset()
        cmd_parser.parse(self.input_line,cmder)
        node_iter.walk(cmder.cmds)

    def input_line(self,cmder,node_iter) :
        self.input_word = ""
        self.input_line = str(cmder)  + " "
        sys.stdout.write(self.input_line )
        self.input_over(cmder,node_iter)
        self.clean_prompt()
        prompt_name_mode   = False
        prompt_value_mode  = False
        with  console_mode() :
            while True:
                    ch = sys.stdin.read(1)
                    if prompt_name_mode :
                        if not ch  == '\t' :
                            self.input_word +=  self.prompt_name
                            self.clean_prompt()
                            prompt_name_mode = False
                    if prompt_value_mode :
                        if not ch  == '=' :
                            self.clean_prompt()
                            prompt_value_mode = False

                    if ch == '=' :
                        args = cmd_parser.parse_args(self.input_word)
                        key  = args.keys()[0]
                        val  = args.values()[0]
                        #pdb.set_trace()
                        if self.find_value_prompt(key,cmder,node_iter) :
                            if self.value_prompt(key,cmder,node_iter) :
                                prompt_value_mode = True
                                if val is not None :
                                    last_clear_len    = len(val)
                                    back_clear(last_clear_len)
                                sys.stdout.write(self.prompt_value)
                                self.input_word = "--%s=%s" %(key,self.prompt_value)
                                continue

                    if ch == '\t' :
                        prompt_name_mode = True
                        last_clear_len = len(self.prompt_name)
                        if self.find_name_prompt(cmder,node_iter) :
                            if self.name_prompt(self.input_word,cmder,node_iter) :
                                back_clear(last_clear_len)
                                sys.stdout.write(self.prompt_name)
                        continue
                    if ch == DEL :
                        #pdb.set_trace()
                        self.input_word = self.input_word[0:-1]
                        back_clear(1)
                        continue

                    if ch == ' ' :
                        self.input_over(cmder,node_iter)
                    if ch == '\r' :
                        self.input_over(cmder,node_iter)
                        return  self.input_line
                    sys.stdout.write(ch)
                    self.input_word += ch
