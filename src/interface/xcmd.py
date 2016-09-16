#coding=utf-8
class commander :
    cmds = []
    args = {}
    def __init__(self,name):
        self.cmds.append(name)
    def show(self):
        print(self)
    def __str__(self):
        cmd = ""
        for c in self.cmds :
            cmd = "%s %s" %(cmd,c)
        for k,v in self.args.items():
            if len(k.strip())  ==  1 :
                cmd = "%s -%s %s" %(cmd,k,v)
            else :
                cmd = "%s --%s=%s" %(cmd,k,v)
        return cmd

    def add_cmd(self,name) :
        self.cmds.append(name)
    def add_arg(self,key,val) :
        self.args[key]  = val
    def reset(self):
        self.cmds = []
        self.args = {}
    def do(self,iter):
        iter.current.do(self)
