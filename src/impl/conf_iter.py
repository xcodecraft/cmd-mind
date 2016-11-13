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

    def next(self,key,strict=False):
        for i in self.current.subs :
            if i.is_match(key,strict) :
                self.save()
                self.parent  = self.current
                self.current = i
                _logger.debug("match %s ,next to :%s" %(key,self.current.name))
                return True
        return False

    def match(self,cmder) :
        _logger.debug("match cmd :%s" %(self.current.name))
        _logger.debug("cmdline :%s" %(cmder))
        self.to_root()
        # import pdb
        # pdb.set_trace()
        for cmd in cmder.cmds :
            if not self.next(cmd,strict=True) :
                return False
        if len (self.current.subs) > 0 :
            return False
        for arg in self.current.args :
            if arg.must :
                if not ( cmder.args.has_key(arg.name) or  ( arg.hotkey != None and  cmder.args.has_key(arg.hotkey) )) :
                    return False
        return True
    def get_prompter(self,word=""):
        _logger.debug("[cmd prompt] current: %s, word:%s" %(self.current.name , word))
        if len(self.current.subs) > 0 :
            return utls.prompt.iter(self.current.subs,word, lambda x: x.name )
        _logger.info("no next cmd prompt ")
        return None

