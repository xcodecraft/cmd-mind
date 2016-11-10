#coding=utf-8
import logging
import utls.prompt 
_logger = logging.getLogger()

class node_iter :
    root    = None
    parent  = None
    current = None

    back_points = []
    def __init__(self,data) :
        self.data = data 
        self.to_root()
    def to_root(self) :
        self.root    = self.data
        self.current = self.data

    def save(self):
        self.back_points.append({"parent" : self.parent, "current" : self.current})

    def back(self):
        saved        = self.back_points.pop()
        self.parent  = saved['parent']
        self.current = saved['current']

    def walk(self,cmds) :
        self.to_root()
        for cmd in cmds :
            _logger.debug("next to %s" %(cmd))
            if not self.next(cmd) :
                return 

    def next(self,key):
        for i in self.current.subs :
            if i.is_match(key) :
                self.save()
                self.parent  = self.current
                self.current = i
                return True
        return False

    def get_prompter(self,word=""):
        _logger.debug("[cmd prompt] current: %s, word:%s" %(self.current.name , word))
        if len(self.current.subs) > 0 :
            return utls.prompt.iter(self.current.subs,word, lambda x: x.name ) 
        return None

