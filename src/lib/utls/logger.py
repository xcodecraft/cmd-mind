import os,string,logging
_logger = logging.getLogger()
def err_log(msg,tag):
    _logger.error("[%s] %s" %(tag,msg))
    

def debug_log(msg,tag=""):
    _logger.debug("[%s] %s" %(tag,msg))

def info_log(msg,tag=""):
    _logger.info("[%s] %s" %(tag,msg))

def info_log(msg,tag=""):
    _logger.info("[%s] %s" %(tag,msg))
