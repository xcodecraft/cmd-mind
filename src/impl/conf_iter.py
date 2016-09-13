#coding=utf-8
class commander :
    cmds = []
    args = {}
    def show(self):
        cmd = ""
        for c in self.cmds :
            cmd = "%s %s" %(cmd,c)
        for k,v in self.args.items():
            cmd = "%s --%s=%s" %(cmd,k,v)
        print(cmd)

class node_iter :
    _root    = None
    _parent  = None
    _current = None
    _back_points = []
    def __init__(self,data,cmder) :
        self._root    = data
        self._current = data
        self.cmder    = cmder
    def save(self):
        self._back_points.append({"parent" : self._parent, "current" : self._current})

    def back(self):
        saved         = self._back_points.pop()
        self._parent  = saved['parent']
        self._current = saved['current']

    def list_next(self) :
        print("----------------")
        for i in self._current.subs :
            i.echo()
            
    def next(self,key):
        for i in self._current.subs :
            if i.is_match(key) :
                i.report(self.cmder)
                self.save()
                self._parent  = self._current
                self._current = i
                break
