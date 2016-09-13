#coding=utf-8
import sys,tty,termios
import binascii


class promptor :
    prompt_list = []
    prompt_index = 0  
    def __init__(self,datalist):
        self.prompt_list.append("123")
        self.prompt_list.append("456")
        #self.prompt_list = datalist 

    def prompt(self,some):
        data = self.prompt_list[self.prompt_index]
        self.prompt_index += 1
        if self.prompt_index >= len(self.prompt_list) :
            self.prompt_index = 0 
        return data

def run(quit,cmdline):
    print("begin...")
    my_promptor = promptor([])
    line        = io.input_line( my_promptor.prompt) 
    print("\r")
    print(line )

class io :
    @staticmethod     
    def input_line(prompt) :   
        line = ""
        word = ""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        BS  = binascii.a2b_hex("08")
        DEL = binascii.a2b_hex("7F")
        ESC = binascii.a2b_hex("1B")
        tty.setraw(sys.stdin.fileno())
        last_bs_len = 0 
        try:
            while True:
                    ch = sys.stdin.read(1)
                    if ch == ' ' :
                        line = line + word + " " 
                        word = ""
                    if ch == '\t' :
                        for i in range(last_bs_len) :
                            sys.stdout.write(BS)
                        data = prompt(word)
                        last_bs_len = len(data)
                        sys.stdout.write(data)
                        word = data 
                        continue
                    if ch == DEL :
                        sys.stdout.write(BS)
                        sys.stdout.write(DEL)
                        sys.stdout.write(BS)
                        continue
                            
                    if ch == '\r' :   
                        line = line +  word 
                        return line
                    sys.stdout.write(ch)    
                    word += ch    
                    last_bs_len = 0 
                    #print binascii.a2b_hex(ch) 
                    

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
