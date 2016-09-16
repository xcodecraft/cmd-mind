#coding=utf-8
import string , logging, sys,os

def set_modul_path() :
    root  = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(root)
    sys.path.append(os.path.join(root,"lib") )
    sys.path.append(os.path.join(root,"interface") )

