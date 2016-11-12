#coding=utf-8
import error,calls
import os,string,logging
import utls.prompt 
_logger = logging.getLogger()
class conf_obj :
    name = ""
    def echo(self):
        print(self.name)
    def is_match(self,key) :
        pass

    def report(self,cmder) :
        pass
    def prompt(self,note_iter,cmder):
        return self.name

class cmd(conf_obj) :
    subs = []
    args = []
    options = []
    call = None
    def is_match(self,key,strict=False) :
        _logger.debug("[is_match] key:%s name:%s" %(key,self.name))
        if key == self.name  :
            return True 
        if strict :
            for x in self.options :
                if key == x :
                    return True 
        else:
            if  self.name == "*" : 
               return True 
        return False 
    def report(self,cmder) :
        cmder.add_cmd(self.name)

    def have_subs(self) :
        return len(self.subs) > 0

    def next_sub(self,cmder) :
        for i in self.subs :
            yield  i 

    def have_args(self) :
        return len(self.args) > 0

    def get_arg(self,key) :
        for i in self.args :
            if i.name == key  or  i.hot == key :
                return i 
            # if hot and i.hot == key :
            #         return i
            # if not hot and i.name == key :
            #         return i
        return None 

    def next_arg(self,cmder) :
        for i in self.args :
            yield i

    def use_arg(self,key,val):
        for i in self.current.args:
            if i.is_match(key) :
                #self.cmder.add_arg(key,val)
                return True
        return False

    def get_prompter(self,key="") :
        _logger.debug("[prompt] cmd : %s" %(self.name))
        if len(self.options) > 0 :
            return utls.prompt.iter(self.options,key, lambda x: x ) 
        return None 

    def args_prompter(self,key="",hot = False) :
        _logger.debug("[prompt] args : %s" %(self.name))
        if len(self.args) > 0 :
            if hot :
                return utls.prompt.iter(self.args,key, lambda x: x.hot ) 
            else:
                return utls.prompt.iter(self.args,key, lambda x: x.name ) 
        return None 

    def do(self,cmder):
        # args = cmder.args
        # map hotkey and name to same value ;
        # for a in self.args :
        #     if a.hotkey is not None :
        #         if a.hotkey in args :
        #             args[a.name] = args[a.hotkey]
        #
        # for arg_obj in self.args:
        #     arg_obj.do(self.name,args[arg_obj.name])

        if self.call is None :
            execmd = str(cmder)
            print("\n%s" %(execmd))
            os.system(execmd)
        # else:
        #     args = cmder.args
        #     try:
        #         calltpl = string.Template(self.call)
        #         execmd = calltpl.substitute(args)
        #         print("\n")
        #         print(execmd)
        #         os.system(execmd)
        #     except KeyError as e :
        #         key = str(e)
        #         msg = "[ %s ] less %s" %(self.call,key)
        #         raise error.icmd_exception(msg)

class arg(conf_obj) :
    hotkey  = None
    value   = None
    default = ""
    values = []
    def do(self,cmd_name,value):
        key = "%s_%s" %(cmd_name,self.name)
        calls.write_history(key,value)
        _logger.debug("load arg[%s] history : %s" %(key,value))

    def is_match(self,key) :
        return key == self.name

    def report(self,cmder) :
        cmder.add_arg(self.name,self.value)

    def prompt_hotkey(self):
        line = "-%s %s" %(self.hotkey, self.default)
        _logger.debug("prompt arg: %s" %line)
        return line

    def prompt_normal(self):
        line = "--%s=%s" %(self.name, self.default)
        _logger.debug("prompt arg: %s" %line)
        return line

    def value_prompter(self,word=""):
        _logger.debug("[prompt] arg : %s" %(self.name))
        if len(self.values) > 0 :
            return utls.prompt.iter(self.values,word, lambda x: x ) 
        return None 

