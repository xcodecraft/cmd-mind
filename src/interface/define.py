#coding=utf-8
import cmd 
class conf_obj :
    name = ""
    def echo(self):
        print(self.name)
    def is_match(self,key) :
        pass

    def report(self,cmder) :
        pass
    def prompt(self):
        return self.name    


class cmd(conf_obj) :
    subs = []
    args = []
    def is_match(self,key) :
        return key == self.name
    def report(self,cmder) :
        cmder.add_cmd(self.name)



class arg(conf_obj) :
    value = None
    default  = None 
    options = []
    def is_match(self,key) :
        return key == self.name

    def report(self,cmder) :
        cmder.add_arg(self.name,self.value)
    def prompt(self):
        line = "--" + self.name 
        if self.default  is not None :
            line = "--" + self.name + "="  + self.default   
        return line     
    def option_next(self) :
        for i in self.options :
            yield i 
