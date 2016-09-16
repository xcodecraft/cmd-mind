#coding=utf-8
class icmd_exception(Exception):
    pass

class bug_exception(Exception) :
    pass

class user_break(icmd_exception):
    pass
class badargs_exception(icmd_exception):
    pass


class var_undefine(icmd_exception):
    pass
