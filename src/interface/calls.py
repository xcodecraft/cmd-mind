#coding=utf-8
import os,os.path
def write_history(key,cmd) :
    home     = os.environ['HOME']
    his_path = "%s/icmd/%s/" %(home,key)
    if not os.path.exists(his_path) :
        os.makedirs(his_path)
    with  file(his_path +"history.log","a+") as fhis :
        fhis.write(cmd + "\n")

def read_history(key):
    home     = os.environ['HOME']
    his_path = "%s/icmd/%s/history.log" %(home,key)
    lines    = []
    if os.path.exists(his_path) :
        with  file(his_path ,"a+") as fhis :
            lines = fhis.readlines(512)
    return lines


