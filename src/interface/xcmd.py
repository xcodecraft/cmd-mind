#coding=utf-8
import impl.cmd_parser
class commander :
    cmds = []
    args = {}
    name = ""
    def __init__(self,name,cmdline = ""):
        self.name = name 
        #self.cmds.append(name)
        impl.cmd_parser.parse(cmdline,self)

    def show(self):
        print(self)
    def __str__(self):
        cmd = self.name
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
