#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging
from subprocess import *
import utls.var_proc


class ExtendTC(unittest.TestCase):
    def test_pipe(self) :
        p = Popen(["/bin/ls" , "/home/zuowenjian/devspace/mara-pub/projects" ], bufsize=1024, stdout=PIPE, close_fds=True)
    def test_var(self) :
        data = utls.var_proc.value_of("${SHELL}")
        self.assertEquals(data,"/bin/bash")
