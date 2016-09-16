#coding=utf-8
import logging
_logger = logging.getLogger()
class node_iter :
    root    = None
    parent  = None
    current = None
    back_points = []
    def __init__(self,data) :
        self.root    = data
        self.current = data
    def save(self):
        self.back_points.append({"parent" : self.parent, "current" : self.current})

    def back(self):
        saved         = self.back_points.pop()
        self.parent  = saved['parent']
        self.current = saved['current']

    def list_subs(self) :
        names = []
        for i in self.current.subs :
            i.echo()
            names.append(i.name)
        return names
    def have_subs(self) :
        return len(self.current.subs) > 0

    def have_args(self) :
        return len(self.current.args) > 0
    def next_sub(self,cmder) :
        for i in self.current.subs :
            yield i.prompt(self,cmder)
    def next_arg(self,cmder) :
        for i in self.current.args :
            if i.name in cmder.args.keys() :
                continue
            yield i.prompt(self,cmder)
    def list_args(self) :
        names = []
        for i in self.current.args :
            i.echo()
            names.append(i.name)
        return names

    def use_arg(self,key,val):
        for i in self.current.args:
            if i.is_match(key) :
                #self.cmder.add_arg(key,val)
                return True
        return False
    def match(self,cmder) :
        self.walk(cmder.cmds)
        if self.match_cmds(cmder)  and self.match_args(cmder) :
            return True
        return False

    def match_cmds(self,cmder) :
        #import pdb
        #pdb.set_trace()
        cmd_len = len(cmder.cmds)
        pnt_len = len(self.back_points) + 1

        if not cmd_len == pnt_len :
            return False
        for idx in range(cmd_len -1 ) :
            cmd     = cmder.cmds[idx]
            point   = self.back_points[idx]
            if not cmd == point['current'].name :
               return False
        curcmd = cmder.cmds[cmd_len -1 ]
        if not curcmd == self.current.name :
                return False
        if len(self.current.subs) > 0 :
            return False
        return True

    def match_args(self,cmder):
         for obj in self.current.args :
             if  not cmder.args.has_key(obj.name) :
                 return False
         return True

    def walk(self,subs):
        for c in subs :
            self.next(c)
    def next(self,key):
        for i in self.current.subs :
            if i.is_match(key) :
                self.save()
                self.parent  = self.current
                self.current = i
                return True
        return False
