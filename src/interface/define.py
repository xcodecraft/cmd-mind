#coding=utf-8
import error,calls
import os,string,logging
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
    call = None
    def is_match(self,key) :
        return key == self.name
    def report(self,cmder) :
        cmder.add_cmd(self.name)

    def do(self,cmder):
        args = cmder.args
        # map hotkey and name to same value ;
        for a in self.args :
            if a.hotkey is not None :
                if a.hotkey in args :
                    args[a.name] = args[a.hotkey]

        for arg_obj in self.args:
            arg_obj.do(self.name,args[arg_obj.name])

        if self.call is None :
            execmd = str(cmder)
            print("\n")
            print(execmd)
            os.system(execmd)
        else:
            args = cmder.args
            try:
                calltpl = string.Template(self.call)
                execmd = calltpl.substitute(args)
                print("\n")
                print(execmd)
                os.system(execmd)
            except KeyError as e :
                key = str(e)
                msg = "[ %s ] less %s" %(self.call,key)
                raise error.icmd_exception(msg)

class arg(conf_obj) :
    hotkey  = None
    value   = None
    default = ""
    options = []
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

    def prompt(self,note_iter,cmder):
        cmd_name = note_iter.current.name
        _logger.debug("prompt arg begin: %s" %cmd_name)
        if self.default  is not None :
            self.default = string.Template(self.default).substitute(cmder.args)
        if len(self.options) == 0 :
            key     = "%s_%s" %(cmd_name,self.name)
            _logger.debug("load arg[%s] history" %key)
            self.options = calls.read_history(cmd_name)
        if self.hotkey is not None :
            return self.prompt_hotkey()
        return self.prompt_normal()

    def option_next(self) :
        if len(self.options) > 0 :
            for i in self.options :
                yield i.strip()

