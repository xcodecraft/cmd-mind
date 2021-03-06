#coding=utf-8
import error,calls
import os,string,logging
import utls.prompt
import copy
from   subprocess import *
from   utls.var_proc import *
from utls.logger import *
_logger = logging.getLogger()
class conf_obj :
    def echo(self):
        print(self.name)
    def on_load(self):
        pass 
    def is_match(self,key) :
        pass
    def report(self,cmder) :
        pass

class load_utls  :
    def do_load_of(self,k) :
        src_dict = self.__dict__
        dst_dict = self.__dict__
        if (src_dict.has_key(k)) :
            if isinstance(src_dict[k],str) :
                ori = src_dict[k] 
                val = utls.var_proc.value_of(ori)
                dst_dict[k] = val
                info_log("self.%s :  %s (%s)" %(k,val,ori),"load")
            if isinstance(src_dict[k],conf_obj) :
                src_dict[k].on_load()

class using(conf_obj) :
    origin  = None 
    cmd     = None
    vars    = {}
    def __getattr__(self,name):
        if self.cmd is not None :
            if  hasattr(self.cmd,name) :
                val = getattr(self.cmd,name)
                debug_log("using cmd.%s : %s"  %(name,val), 'using')
                return val 
        raise AttributeError()

    def echo(self):
        pass
    def on_load(self):
        for k,v in self.vars.items() :
            os.environ[k] = v  
            info_log("set %s =  %s" %(k,v) ,"load")
        self.cmd = copy.deepcopy(self.origin)
        self.cmd.on_load()
    def is_match(self,key,strict=False) :
        return self.cmd.is_match(key,strict)
    def report(self,cmder) :
        return self.cmd.report()
    def help(self,cmdlevel=1) :
        return self.cmd.help(cmdlevel)
    def check(self) :
        return self.cmd.check()

class cmd(conf_obj,load_utls) :
    subs    = []
    args    = []
    vars    = {}
    options = None
    call    = None
    name    = ""

    def on_load(self):
        info_log("cmd %s" %(self) ,"load")
        for k,v in self.vars.items() :
            os.environ[k] = v  
            info_log("set %s =  %s" %(k,v) ,"load")
        self.do_load_of('call')
        self.do_load_of('name')
        for sub in self.subs :
            sub.on_load()

        for arg in self.args :
            arg.on_load()


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
        return "{0:10} {1} {2}".format(mainmsg,subsmsg,argsmsg)

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
        # import pdb
        # pdb.set_trace()
        for arg in self.args:
            val = None
            if cmder.args.has_key(arg.name) :
                val = cmder.args[arg.name]
            if cmder.args.has_key(arg.hotkey) :
                val = cmder.args[arg.hotkey]
            if arg.must == False and val == None :
                info_log("ignore arg %s" %(arg.name),'do')
                continue
            execmd  = "%s %s" %(execmd, arg.getcmd(val))
        info_log("cmd: %s" %(execmd),'do')
        print("\n%s" %execmd)
        os.system(execmd)

class arg(conf_obj,load_utls) :
    hotkey  = None
    value   = None
    must    = False
    default = None
    values  = None
    call    = None
    def on_load(self) :
        self.do_load_of('default') 
        self.do_load_of('values') 
        self.do_load_of('call') 

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
                debug_log(self.call,'call')
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
        if values is None : 
            return []
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

class pipe(conf_obj,load_utls) :
    cmd = None
    args = ""
    def on_load(self) :
        self.do_load_of('cmd')
        self.do_load_of('args')
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
