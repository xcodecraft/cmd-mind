#coding=utf-8
class console_exception(Exception):
    pass

class bug_exception(Exception) :
    pass

class user_break(console_exception):
    pass
class badargs_exception(console_exception):
    pass

class cmd_use_error(console_exception):
    def __init__(self,cmd,message):
        self.cmd = cmd
        rigger_exception.__init__(self,message)

class depend_exception(console_exception) :
    def __init__(self,monitor):
        self.monitor = monitor
    pass

class var_undefine(console_exception):
    pass
