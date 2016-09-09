import  re , os , string ,  getopt ,sys , unittest,logging


def setup_env() :
    root  = os.path.dirname(os.path.realpath(__file__))
    root  = os.path.dirname(root)
    sys.path.append(os.path.join(root,"src") )
    import core.run_env
    core.run_env.set_modul_path()

    os.environ['PRJ_ROOT'] = os.environ['HOME'] + "/devspace/pylon-console"
    logging.basicConfig(level=logging.DEBUG,filename='test.log')


if __name__ == '__main__':
    from testcase import *

    unittest.main()
