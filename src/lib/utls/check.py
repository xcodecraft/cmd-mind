#coding=utf-8
import os
import error

def not_none(val,errmsg) :
    if val is None :
        raise error.icmd_exception( errmsg )
    return val

def must_true(val,errmsg) :
    if not val ==  True :
        raise error.icmd_exception( errmsg )
    return val

def ok(val,errmsg) :
    if not val :
        raise error.icmd_exception( errmsg )
    return val
def must_exists( path) :
    if path is None or not os.path.exists(path) :
        raise error.icmd_exception("file not exists : %s" %path )

