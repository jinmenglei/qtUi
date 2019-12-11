import time
#
import tracemalloc
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

import psutil

from base.U_dispatcher import UDispatcher
from base.U_log import get_logger
from base.U_msg import UMsg
import roslaunch
from usher.ros_start.launchStart import LaunchThread
from multiprocessing import Process

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
    ditNet = psutil.net_if_addrs()

    if '192.168.' in str(ditNet):
            return True
    return False


def get_ros_core():
    pid = psutil.process_iter()
    for pid_sub in pid:
        if 'roscore' == pid_sub.name():
            print('get roscore')
            return True
    return False


def get_pid_by_name(name: str):
    pid = psutil.process_iter()
    for pid_sub in pid:
        if name == pid_sub.name():
            print('get ' + str(name))
            return True
    return False


class RosManager(object):
    def __init__(self, manager_pipe):
        self.__module_name = 'ros_manager'
        self.__logger = get_logger(self.__module_name)
        self.dispatcher = UDispatcher(UMsg.ros_dispatcher, manager_pipe)
        self.launch_thread = None

    def ros_core_process(self):
        self.__logger.info('begin ros core')
        while True:
            while True:
                time.sleep(3)
                if getipaddr():
                    self.__logger.info('host ip is init!')
                    break

            if not get_ros_core():
                self.__logger.info('start ros core')
                try:
                    roslaunch.main(['roscore', '--core'])
                    while True:
                        time.sleep(1)
                except roslaunch.RLException as e:
                    print('I am except')
                    self.__logger.fatal(str(e))
                    continue

                finally:
                    self.__logger.fatal('I am finally')

            else:
                self.__logger.warning('ros core is exist , skip!')
                break

    def start(self):
        self.__logger.info('begin to init ros core')

        process = Process(target=self.ros_core_process)
        process.start()

        self.launch_thread = LaunchThread()
        self.launch_thread.run()


#  test code
if __name__ == '__main__':
    pid = psutil.process_iter()
    for pid_sub in pid:
        if 'roscore' == pid_sub.name():
            print('get roscore')
    pass