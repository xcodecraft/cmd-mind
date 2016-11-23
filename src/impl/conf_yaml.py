#coding=utf8
import re , os , yaml, logging
# import interface
import utls.dbc, utls.var_proc
# from utls.rg_io import rg_logger



def load_conf(conf_path,ori,new) :
    l = loader(conf_path)
    return l.load_data(ori,new)


class loader:
    def  __init__(self,conf):
        self.conf    = conf
        utls.dbc.must_exists(self.conf)
        self.curpath = os.path.dirname(self.conf)
        logging.getLogger().debug("yaml current path:%s" %self.curpath)
    def load(self):
        utls.dbc.must_exists(self.conf)
        doc = open(self.conf,"r").read()
        return doc

    def load_data(self,ori=None,new=None):
        doc = self.load()
        if ori is not None:
            doc = doc.replace(ori,"!!python/object:" + new)
        doc  = utls.var_proc.value_of(doc) 
        data = yaml.load(doc)
        return data['main']
