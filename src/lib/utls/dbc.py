#coding=utf-8
import os
import error
def not_none(val,errmsg) :
    if val is   None :
        raise error.bug_exception( errmsg )
    return val

def must_true(val,errmsg) :
    if not val ==  True :
        raise error.bug_exception( errmsg )
    return val
def must_exists( path) :
    if path is None or not os.path.exists(path) :
        raise error.bug_exception("file not exists : %s" %path )

def must_obj(val,cls):
    if not isinstance(val,cls) :
        raise error.bug_exception( " is not %s instance" %cls.__name__)
    return val

