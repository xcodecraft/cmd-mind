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

def complement(cmder,node_iter):
    pio         = prompt_io()
    line        = pio.input( cmder,node_iter)

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

class io_status:
    tag_sep = " "
    tag_ass = "="
    tag_mpt = "="
    tag_quote ='"'
    mode_cmd        = "mode_cmd"
    mode_arg_key    = "mode_arg_key"
    mode_arg_val    = "mode_arg_val"
    mode_unknow     = "mode_unknow"
    mode_prompt     = "mode_prompt"
    mode_assgin     = "mode_assgin"
    mode_quote      = "mode_quote"
    pre_mode        = None
    cur_mode        = ""
    def is_cmd(self)  :
        return self.cur_mode == self.mode_cmd
    def to_cmd(self)  :
        self.cur_mode = self.mode_cmd

    def is_unknow(self) :
        return self.cur_mode == self.mode_unknow
    def to_unknow(self) :
        self.cur_mode = self.mode_unknow

    def is_quote(self)  :
        return self.cur_mode == self.mode_quote

    def to_quote(self) :
        self.pre_mode = self.cur_mode
        self.cur_mode = self.mode_quote

    def to_back(self) :
        self.cur_mode = self.pre_mode
        self.pre_mode = None

    def is_prompt(self) :
        return self.cur_mode == self.mode_prompt
    def to_prompt(self) :
        self.pre_mode = self.cur_mode
        self.cur_mode = self.mode_prompt

    def is_assgin(self) :
        return self.cur_mode == self.mode_assgin
    def to_assgin(self) :
        self.pre_mode = self.cur_mode
        self.cur_mode = self.mode_assgin

    def is_arg_key(self):
        return self.cur_mode == self.mode_arg_key

    def is_arg_val(self):
        return self.cur_mode == self.mode_arg_val

    def to_arg_key(self):
        self.cur_mode = self.mode_arg_key
    def to_arg_val(self):
        self.cur_mode = self.mode_arg_val



class prompt_io :
    name_iter    = None
    value_iter   = None
    prompt_block  = ""
    prompt_value = ""
    input_line   = ""
    input_word   = ""
    input_status = []

    def get_promptor(self,cmder,node_iter) :
        prompt_iter = None
        if (not node_iter.match_cmds(cmder) ) and node_iter.have_subs() :
            prompt_iter = node_iter.next_sub(cmder)
            _logger.debug("cmd prompt")
        elif (not node_iter.match_args(cmder) ) and node_iter.have_args() :
            prompt_iter = node_iter.next_arg(cmder)
            _logger.debug("arg prompt")
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
            except StopIteration:
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
                    self.prompt_block = p_word
                    _logger.debug("prompt: %s" %self.prompt_block)
                    return True
            except StopIteration:
                self.name_iter = None
                if stop_count > 10 :
                    return False
                stop_count += 1
                if not self.find_name_prompt(cmder,node_iter) :
                    return False


    def clean_prompt(self):
        self.name_iter      = None
        self.value_iter     = None
        self.prompt_block    = ""
        self.prompt_value   = ""

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

    def record_char(self,ch) :
        sys.stdout.write(ch)
        self.input_line =  self.input_line + ch
        self.input_status.append(self.status)

    def record_word(self,word) :
        for c in word:
            self.record_char(c)

    def reback_char(self) :
        back_clear(1)
        self.input_line = self.input_line[0:-1]
        self.input_status.append(self.status)
        self.status = self.input_status.pop()

    def reback_word(self,word) :
        for c in word:
            self.reback_char()

    def input(self,cmder,node_iter) :
        self.auto_buffer =  str(cmder)
        self.status = io_status()
        self.status.to_unknow()
        with  console_mode() :
            while True:
                    ch = self.get_char()
                    _logger.debug("mode:%s ,char:%s" %(self.status.cur_mode,ch))
                    if ch == '\r' :
                        self.input_over(cmder,node_iter)
                        return  self.input_line
                    if self.status.is_quote() :
                        if not ch == '"' :
                            self.status.to_back()
                        self.record_char(ch)
                        continue

                    if self.status.is_prompt() :
                        if not ch  == ' ' :
                            self.status.to_back()
                        if ch == '\t' :
                            if self.find_name_prompt(cmder,node_iter) :
                                _logger.debug("found name promptor")
                                last_prompt   = self.prompt_block
                                if self.name_prompt(self.input_word,cmder,node_iter) :
                                    self.reback_word(last_prompt)
                                    self.record_word(self.prompt_block)
                        continue

                    if self.status.is_assgin():
                        if not ch  == ' ' :
                            self.status.to_back()
                        if ch == '=' :
                            if self.find_value_prompt(arg_key,cmder,node_iter) :
                                _logger.debug("found value promptor")
                                last_assgin = self.prompt_value
                                if self.value_prompt(arg_key,cmder,node_iter) :
                                        _logger.debug("clean %s" %last_assgin)
                                        self.reback_word(last_assgin)
                                        self.record_word(self.prompt_value)
                        continue
                    if self.status.is_arg_val():
                        if ch == '=' :
                            if self.find_value_prompt(arg_key,cmder,node_iter) :
                                _logger.debug("found value promptor")
                                if self.value_prompt(arg_key,cmder,node_iter) :
                                        self.record_word(self.prompt_value)
                                        self.status.to_assgin()
                        if ch == '"' :
                            self.record_char(ch)
                            self.status.to_quote()
                            continue
                        if ch == DEL :
                            self.reback_char()
                            continue
                        if ch == ' ' :
                            self.status.to_unknow()
                        self.record_char(ch)



                    if self.status.is_arg_key():
#disable
                        if ch == '"' :
                            continue
                        if ch == ' ' :
                            self.status.to_arg_val()
                        if ch == '=' :
                            self.status.to_arg_val()
                        if ch == DEL :
                            self.reback_char()
                            continue
                        self.record_char(ch)
                        continue

                    if self.status.is_unknow():
                        if ch == '\t' :
                            if self.find_name_prompt(cmder,node_iter) :
                                _logger.debug("found name promptor")
                                if self.name_prompt(self.input_word,cmder,node_iter) :
                                    self.record_word(self.prompt_block)
                                    self.status.to_prompt()
                            continue
                        if ch == '-' :
                            self.status.to_arg_key()
                        if ch == DEL :
                            self.reback_char()
                            continue
                        self.record_char(ch)
