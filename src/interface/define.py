#coding=utf-8
import error,calls
import os,string,logging
import utls.prompt
from   subprocess import *
from   utls.var_proc import *
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
    def conf(self):
        pass

class cmd(conf_obj) :
    subs    = []
    args    = []
    options = None
    call    = None
    name    = ""

    def conf(self):
        os.environ['_CMD_NAME'] = self.name
        for sub in self.subs :
            sub.conf()

    def help(self,cmdlevel=1):
        mainmsg = "%s" %(self.name)
        if self.name.strip() == "*" :
            optmsg = ""
            for opt in self.options :
                optmsg = "%s/%s" %(optmsg,opt)
            mainmsg = optmsg

        subsmsg = ""
        argsmsg = ""
        if len(self.subs) >0 :
            i = 0 
            for sub in self.subs :
                subsmsg = "{0}\n{1:{width}}{2}".format(subsmsg,' ',sub.help(cmdlevel+1),width=cmdlevel * 5 )
                if i == 3 : 
                    break
                i = i + 1
        else: 
            for arg in self.args :
                argsmsg  = "%s %s" %(argsmsg,arg.help())
        return "{0:10} {1} {2:10}".format(mainmsg,subsmsg,argsmsg)

    def check(self) :
        if not type(self.subs) == type([]) :
            raise error.icmd_exception("%s.subs is not  []  " %(self.name))
        if not type(self.args) == type([]) :
            raise error.icmd_exception("%s.args is not  []  " %(self.name))
        if self.name == "" :
            raise error.icmd_exception("cmd not set name" %(self.name))

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
        if options == None :
            return []
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
        for arg in self.args:
            val = None
            if cmder.args.has_key(arg.name) :
                val = cmder.args[arg.name]
            if cmder.args.has_key(arg.hotkey) :
                val = cmder.args[arg.hotkey]
            if arg.must == False and val == None :
                continue
            execmd  = "%s %s" %(execmd, arg.getcmd(val))
        _logger.info("cmd: %s" %(execmd))
        print("\n%s" %execmd)
        os.system(execmd)

class arg(conf_obj) :
    hotkey  = None
    value   = None
    must    = False
    default = None
    values  = None
    call    = None
    def help(self) :
        msg = ""
        if self.hotkey is not None :
            msg = "-%s <%s>" %(self.hotkey,self.name)
        else :
            msg = "--%s <%s>" %(self.name,self.name)
        if not self.must :
           msg =  "[ %s ]" %(msg)
        return msg 
    def is_match(self,key) :
        return key == self.name
    def getcmd(self,val) :
        if val == None:
            if isinstance(self.default, pipe) :
                vals = self.default.get()
                if len(vals) > 0 :
                    val = vals[0].strip()
        if val == None :
            raise error.icmd_exception("arg %s not set value" %(self.name))
        if self.call is None :
            return "--%s %s" %(self.name,val)
        else:
            try :
                return string.Template(self.call).substitute({self.name : val})
            except :
                raise error.icmd_exception("error! args call:[%s], but key is: %s"%(self.call,self.name))

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
        _logger.warn("[prompt] not values ")
        return None

class pipe(conf_obj) :
    cmd = None
    args = ""
    def get(self) :
        self.cmd  = value_of(self.cmd,'&')
        self.args = value_of(self.args,'&')

        if not os.path.exists(self.cmd) :
            raise error.icmd_exception("cmd is not exists : %s" %(self.cmd))
        args = self.args.split(' ')
        args = [self.cmd] + args
        _logger.info("cmd: %r"  %(args) )
        p = Popen(args , bufsize=1024, stdout=PIPE, close_fds=True)
        return p.stdout.readlines()
