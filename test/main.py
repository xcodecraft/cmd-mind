import  re , os , string ,  getopt ,sys , unittest,logging


def setup_env() :
    root  = os.path.dirname(os.path.realpath(__file__))
    root  = os.path.dirname(root)
    sys.path.append(os.path.join(root,"src") )
    import xenv
    xenv.set_modul_path()

    os.environ['PRJ_ROOT'] = os.environ['HOME'] + "/devspace/pylon-console"
    logging.basicConfig(level=logging.DEBUG,filename='test.log')


if __name__ == '__main__':
    setup_env()
    from testcase.conf_tc import *
    from testcase.parse_tc import *
    from testcase.calls_tc import *
    from testcase.io_tc import *
    from testcase.mode_tc import *
    from testcase.prompt_tc import *

    unittest.main()
