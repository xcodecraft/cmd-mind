#coding=utf-8
import  re , os , string ,  getopt ,sys , unittest,logging
from subprocess import *


class ExtendTC(unittest.TestCase):
    def test_pipe(self) :
        # p = Popen(["/bin/ls" "/home/zuowenjian/devspace/mara-pub/projects" ], bufsize=1024, stdout=PIPE, close_fds=True)
        p = Popen(["/bin/ls" , "/home/zuowenjian/devspace/mara-pub/projects" ], bufsize=1024, stdout=PIPE, close_fds=True)
        # fout =  p.stdout
        # print fout.readlines(),
        # for i in range(10):
        #     fin.write("line" + str(i))
        #     fin.write('\n')
        #     fin.flush()
        #     print fout.readline(),

