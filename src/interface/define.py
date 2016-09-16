#coding=utf-8
import error
import os,string
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
    call = None
    def is_match(self,key) :
        return key == self.name
    def report(self,cmder) :
        cmder.add_cmd(self.name)

    def do(self,cmder):
        if self.call is None :
            execmd = str(cmder)
            print("\n")
            print(execmd)
            os.system(execmd)
        else:
            args = cmder.args
            # map hotkey and name to same value ;
            for a in self.args :
                if a.hotkey is not None :
                    if a.hotkey in args :
                        args[a.name] = args[a.hotkey]

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
    default = None
    options = []
    def is_match(self,key) :
        return key == self.name

    def report(self,cmder) :
        cmder.add_arg(self.name,self.value)

    def prompt_hotkey(self):
        line = "-%s " %(self.hotkey)
        if self.default  is not None :
            line = "-%s %s" %(self.hotkey, self.default)
        return line

    def prompt_normal(self):
        line = "--%s=" %(self.hotkey)
        if self.default  is not None :
            line = "--%s=%s" %(self.hotkey, self.default)
        return line

    def prompt(self):
        if self.hotkey is not None :
            return self.prompt_hotkey()
        return self.prompt_normal()

    def option_next(self) :
        for i in self.options :
            yield i
