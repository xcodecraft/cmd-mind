#coding=utf-8
import error,calls
import os,string,logging
import utls.prompt
from subprocess import *
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
    options = None
    call = None
    def is_match(self,key,strict=False) :
        _logger.debug("[is_match] key:%s name:%s" %(key,self.name))
        if key == self.name  :
            return True
        if strict :
            for x in self.get_options():
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
            if i.name == key  or  i.hotkey == key :
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

    def get_options(self):
        options = self.options
        if isinstance(self.options , pipe) :
            options = self.options.get()
        return options
    def get_prompter(self,key="") :
        _logger.debug("[prompt] cmd : %s" %(self.name))
        options = self.get_options()
        if len(options) > 0 :
            return utls.prompt.iter(options,key, lambda x: x )
        return None

    def args_prompter(self,key="",hot = False) :
        _logger.debug("[prompt] args : %s" %(self.name))
        if len(self.args) > 0 :
            if hot :
                return utls.prompt.iter(self.args,key, lambda x: x.hotkey )
            else:
                return utls.prompt.iter(self.args,key, lambda x: x.name )
        return None

    def getcmd(self) :
        if self.call is None :
            return name
        else :
            return self.call

    def do(self,cmder):

        execmd =  self.getcmd()
        for key,val in cmder.args.items() :
            arg = self.get_arg(key)
            execmd  = "%s %s" %(execmd, arg.getcmd(val))
        _logger.info("cmd: %s" %(execmd))
        print("\n%s" %execmd)
        os.system(execmd)

class arg(conf_obj) :
    hotkey  = None
    value   = None
    must    = False
    default = ""
    values = None
    def do(self,cmd_name,value):
        key = "%s_%s" %(cmd_name,self.name)
        calls.write_history(key,value)
        _logger.debug("load arg[%s] history : %s" %(key,value))

    def is_match(self,key) :
        return key == self.name
    def getcmd(self,val) :
        if self.call is None :
            return "--%s %s" %(self.name,val)
        else:
            return string.Template(self.call).substitute({self.name : val})

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

    def get_values(self):
        values = self.values
        if isinstance(self.values , pipe) :
            values = self.values.get()
        return values
    def value_prompter(self,word=""):
        _logger.debug("[prompt] arg : %s" %(self.name))
        values = self.get_values()
        if len(values) > 0 :
            return utls.prompt.iter(values,word, lambda x: x )
        _logger.warnning("[prompt] not values ")
        return None

class pipe(conf_obj) :
    cmd = None
    args = ""
    def get(self) :
        if not os.path.exists(self.cmd) :
            raise error.icmd_exception("cmd is not exists : %s" %(self.cmd))
        p = Popen([self.cmd,self.args ], bufsize=1024, stdout=PIPE, close_fds=True)
        return p.stdout.readlines()
