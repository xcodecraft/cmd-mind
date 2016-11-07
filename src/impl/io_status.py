#coding=utf-8
import sys,tty,termios
import binascii
import cmd_parser,calls
import pdb
import logging

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
