#coding=utf-8
import string , logging, sys,os
import yaml


def load_conf():
    pass

def load_rgenv():
    import  setting,rg_env,utls.rg_var
    rg_env.rgenv_enable()
    utls.rg_var.import_dict(setting.rgenv)

def set_modul_path() :
    root  = os.path.dirname(os.path.realpath(__file__))
    root  = os.path.dirname(root)
    sys.path.append(root)
    sys.path.append(os.path.join(root,"lib") )

