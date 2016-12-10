#coding=utf-8
import sys,tty,termios
import binascii
import cmd_parser,calls
import pdb
import logging

BS  = binascii.a2b_hex("08")
DEL = binascii.a2b_hex("7F")
ESC = binascii.a2b_hex("1B")
END_KEY     = '\r'

_logger = logging.getLogger()


class console_io :
    def __init__(self):
        self.input = "" 
    @staticmethod    
    def back(char_len) :
        for i in range(char_len) :
            sys.stdout.write(BS)
            sys.stdout.write(DEL)
            sys.stdout.write(BS)
            
    def reback(self) :
        console_io.back(1)
        self.input= self.input[0:-1]
        #self.input_status.append(self.status)
        #self.status = self.input_status.pop(            
    def record(self,ch) :
        _logger.debug("[%s] record: %s" %(self.__class__.__name__ ,ch) )
        sys.stdout.write(ch)
        self.input =  self.input + ch
        
        #self.input_status.append(self.status            

    def reback_word(self,word) :
        for c in word:
            self.reback()
            
    def record_word(self,word) :
        for c in word:
            self.record(c)

class io_god :
    def __init__(self) :
        self.block = None 
        self.input = "" 
    def chose_block(self,c) :
        if ' ' == c :
            return empty_io()
        if '-' == c :
            return args_io()
        return cmd_io()         
           
    def io(self,c) :
        if c == END_KEY :
            self.input += self.block.input
        if self.block == None :
            self.block = self.chose_block(c) 
        if not self.block.io(c):    
            self.input = self.input + self.block.input + c 
            self.block = None 

class empty_io (console_io ):
    def io(self,c) :
        return False 
        
class cmd_io (console_io ):
    prompt_mode = 1 
    input_mode  = 2 
    prompt_key  = '\t'
    prompter = None 
    mode = 0 
    def __init__(self):
        console_io.__init__(self)
        self.mode = cmd_io.input_mode 
        self.last_prompt= ""
    def io_prompt(self,c) :    
            if ' ' == c :
                return False
            if c == cmd_io.prompt_key :
                self.reback_word(self.last_prompt)
                prompt = cmd_io.prompter(self,self.input)
                self.record_word(prompt)
                self.last_prompt = prompt  
                return True 
            self.last_prompt = ""     
            self.record(c) 
            self.mode = cmd_io.input_mode      
            return True     
    def io_input(self,c):
        if ' ' == c :
            return False
        if c == DEL :
            if len(self.input) == 0 :
                return False 
            self.reback()
            return True 
        if c == cmd_io.prompt_key :
            prompt = cmd_io.prompter(self,self.input)
            self.record_word(prompt)
            self.last_prompt = prompt  
            self.mode  =  cmd_io.prompt_mode 
            return True 
        self.record(c) 
        return  True
    def io(self,c) :
        if cmd_io.prompt_mode == self.mode :
            return self.io_prompt(c)
        if cmd_io.input_mode == self.mode :    
            return self.io_input(c)
        self.record(c) 
        return  True

class args_io(console_io) :
    mode           =  0 
    mode_input_key = 1
    mode_input_val = 2
    mode_prompt    = 3
    key_key_end    = ' '
    key_val_end    = ' '

    def __init__(self):
        console_io.__init__(self)
        self.mode = args_io.mode_input_key
        self.last_prompt= ""

    def io(self,c)  :
        #import pdb 
        #pdb.set_trace()
        if args_io.mode_prompt == self.mode :
            return self.io_prompt(c)
        if args_io.mode_input_key == self.mode :    
            if self.io_key(c) :
                return True 
        if args_io.mode_input_val == self.mode :    
            if self.io_val(c) :
                return True
        self.record(c) 
        return  False
    def io_key(self,c):    
        if self.key_key_end == c :
            self.mode = args_io.mode_input_val
            return False
        if '-' == c :
            self.key_key_end = '='   
        if c == DEL :
            if len(self.input) == 0 :
                return False 
            self.reback()
            return True 
        #if c == args_io.prompt_key :
        #    prompt = cmd_io.prompter(self,self.input)
         #   self.record_word(prompt)
          #  self.last_prompt = prompt  
           # self.mode  =  cmd_io.prompt_mode 
            #return True 
        self.record(c) 
        return  True
        
        pass
    def io_val(self,c):    
        if self.key_val_end == c :
            return False 
        if '\t' == c :
            self.mode = self.mode_prompt 
            return True    
        self.record(c) 
        return  True
        
    def io_prompt(self,c):    
        pass
    
