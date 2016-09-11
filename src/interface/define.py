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

class conf_obj :
    name = ""
    subs = []
    def echo(self):
        print(self.name)
    def is_match(self,key) :
        pass

    def report(self,cmder) :
        pass


class cmd(conf_obj) :
    def is_match(self,key) :
        return key == self.name
    def report(self,cmder) :
        cmder.cmds.append(self.name)



class arg(conf_obj) :
    value = None
    def is_match(self,val) :
        args       = val.split("=")
        key        = args[0].strip()
        if len(args) == 2 :
            self.value = args[1].strip()
        long_key  = "--%s" %(self.name)
        short_key = "-%s" %(self.name)
        if  key == long_key or key == short_key :
            return True
        return False

    def report(self,cmder) :
        cmder.args[self.name] = self.value
