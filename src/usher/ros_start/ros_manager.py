import time
#
import tracemalloc
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

import psutil
import subprocess

from base.U_dispatcher import UDispatcher
from base.U_log import get_logger
from base.U_msg import UMsg
import roslaunch
from usher.ros_start.launchStart import LaunchThread
from multiprocessing import Process
from third_party.config import get_value_by_key

host_ros = ('0.0.0.0', 8891)


# mem test
def get_mem_snap():
    # test mem
    server = HTTPServer(host_ros, Resquest_ros)
    print("Starting server, listen at: %s:%s" % host_ros)
    task = Thread(target=server.serve_forever)
    task.start()
    global snap_finsh
    snap_finsh = False
    time.sleep(20)

    global snapshot_ros
    tracemalloc.start()
    snapshot_ros = tracemalloc.take_snapshot()
    snap_finsh = True


class Resquest_ros(BaseHTTPRequestHandler):
    def do_GET(self):
        if snap_finsh:
            snapshot2 = tracemalloc.take_snapshot()
            top_stats = snapshot2.compare_to(snapshot_ros, 'lineno')
            self.send_response(200)
            # self.send_header('Content-type', 'application/json')
            data = str(top_stats).replace('>, <', '> \r\n <')
        else:
            data = 'not init'
        self.wfile.write(bytes(data.encode('utf-8')))
# mem test


def getipaddr():
    ditNet = subprocess.getoutput('ifconfig')

    if '192.168.' in str(ditNet):
            return True, ditNet
    return False, ditNet


def get_pid_by_name(name: str):
    pid = psutil.process_iter()
    for pid_sub in pid:
        if name == pid_sub.name():
            print('get ' + str(name))
            return True
    return False


def get_ros_core():
    return get_pid_by_name('roscore') or get_pid_by_name('rosmaster')


class RosManager(object):
    def __init__(self, module_pipe):
        self.__module_name = 'ros_manager'
        print('come in ' + str(self.__module_name))
        try:
            self.__logger = get_logger(self.__module_name)
            print('come in 78' + str(self.__module_name))
            self.__logger.info('come in ' + self.__module_name)
            print('come in 80' + str(self.__module_name))
            self.dispatcher = UDispatcher(UMsg.ros_dispatcher, module_pipe)
            print('come in 82' + str(self.__module_name))
        except Exception as e:
            import os
            os.system('echo \"' + str(e) + '\" > coredump.log')
            self.__logger.fatal('find exception: ' + str(e))

        self.__logger.info('UDispatcher init ok ')
        self.launch_thread = None
        self.__logger_inner = None

    def ros_core_process(self):
        logger_inner = get_logger('ros_manager_inner')
        logger_inner.info('begin ros core')
        try:
            while True:
                while True:
                    time.sleep(3)
                    status, result = getipaddr()
                    logger_inner.info('get ip :' + str(result))
                    if status:
                        logger_inner.info('host ip is init!')
                        break
                    else:
                        print('wait for ip init!!')
                        logger_inner.warning('wait for ip init!!')

                if not get_ros_core():
                    logger_inner.info('start ros core')
                    try:
                        roslaunch.main(['roscore', '--core'])
                        while True:
                            time.sleep(1)
                    except Exception as e:
                        print('I am except ' + str(e))
                        logger_inner.fatal(str(e))
                        continue

                    finally:
                        logger_inner.fatal('I am finally')
                        time.sleep(1)

                else:
                    logger_inner.warning('ros core is exist , skip!')
                    print('ros core is exist , skip!')
                    break
        except Exception as e:
            print('something error ' + str(e))
            logger_inner.fatal('something error ' + str(e))

    def start(self):
        self.__logger.info('begin to init ros core')
        try:
            process = Process(target=self.ros_core_process)
            process.daemon = True
            time.sleep(1)
            process.start()
            self.__logger.info('complete to init ros core')

            check_memory = get_value_by_key('check_memory', 'CONFIG')
            self.__logger.info('get check_memory :' + str(check_memory))
            if check_memory == 'yes':
                task_mem = Thread(target=get_mem_snap)
                task_mem.start()

            self.launch_thread = LaunchThread()
            self.launch_thread.start()

        except Exception as e:
            self.__logger.fatal('process start fail!! ' + str(e))
            time.sleep(1)



#  test code
if __name__ == '__main__':
    pid = psutil.process_iter()
    for pid_sub in pid:
        if 'roscore' == pid_sub.name():
            print('get roscore')
    pass