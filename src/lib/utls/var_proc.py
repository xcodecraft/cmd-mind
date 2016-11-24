#coding=utf-8
import sys,re,os,string,logging
import error
_logger = logging.getLogger()




class ignore_exp:
    def __init__(self,ignore) :
        self.ori = assigner._ignore 
        assigner._ignore  = re.compile(ignore) 
    def __enter__(self):
        pass
    def __exit__(self,*args,**kwargs):
        assigner._ignore = self.ori
class assigner :
    _ignore = re.compile("^$")
    def __init__(self,tpl,vardict):
        self.tpl          = tpl
        self.vardict      = vardict
    def assign_value(self,match):
        var= str(match.group(1))
        var=var.upper()
        while True:
                if self.vardict.has_key(var) :
                    val  = self.vardict[var]
                    return val
                else :
                    raise  error.var_undefine("%s not define in [%s]" %(self.tpl,var))


def value_of(string,flag='$'):
    tpl     = string
    var_exp = re.compile("\%s\{(\w+)\}" %(flag))
    ass     = assigner(tpl,os.environ)
    try :
        while var_exp.search(tpl):
            tpl = var_exp.sub(ass.assign_value,tpl)
    except TypeError as e :
        raise error.icmd_exception(tpl + "tpl proc fail!")
    return tpl

