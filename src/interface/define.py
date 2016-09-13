
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
