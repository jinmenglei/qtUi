from base.U_msg import UMsg
from base.U_log import get_logger
from usher.service.interface_ros import InterfaceRos
from usher.service.video_record import VideoRecord
from usher.service.Update_task import UpdateTask
from base.U_dispatcher import UDispatcher
from usher.service.cfg_server import CfgServer
import time
from third_party.config import get_value_by_key

# test mem
import tracemalloc
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
host_server = ('0.0.0.0', 8890)

# mem test
def get_mem_snap():
    # test mem
    server = HTTPServer(host_server, Resquest_server)
    print("Starting server, listen at: %s:%s" % host_server)
    task = Thread(target=server.serve_forever)
    task.start()
    global snap_finsh
    snap_finsh = False
    time.sleep(20)

    global snapshot_server
    tracemalloc.start()
    snapshot_server = tracemalloc.take_snapshot()
    snap_finsh = True
    return


class Resquest_server(BaseHTTPRequestHandler):
    def do_GET(self):
        if snap_finsh:
            snapshot2 = tracemalloc.take_snapshot()
            top_stats = snapshot2.compare_to(snapshot_server, 'lineno')
            self.send_response(200)
            # self.send_header('Content-type', 'application/json')
            data = str(top_stats).replace('>, <', '> \r\n <')
        else:
            data = 'not init'
        self.wfile.write(bytes(data.encode('utf-8')))
        return
# mem test


class ServiceManger(object):
    """
    服务的管理模块,显示和业务分开,其实是ros需要主线程,ui也是,所以
    目前包括:
    ros
    行车记录仪
    更新
    """
    def __init__(self, manager_pipe):
        self.module_name = 'service_manager'

        self.__logger = get_logger(self.module_name)
        self.__logger.info('init ' + str(self.module_name) + ' begin')
        print('come in 61')
        try:
            print('come in 63')
            self.dispatcher = UDispatcher(UMsg.service_dispatcher, manager_pipe)
            print('come in 65')
        except Exception as e:
            print('come in 65')
            self.__logger.fatal('find exception : ' + str(e))
        self.__logger.info('init ' + str(self.module_name) + ' success')
        return

    def start(self):
        self.__logger.info('start service_manger!')
        cfg_server = CfgServer()
        cfg_server.start()
        self.__logger.info('start cfg_service ok!')
        interface_ros = InterfaceRos()
        interface_ros.start()
        self.__logger.info('start interface_ros ok')
        video_record_enable = get_value_by_key('video_record_enable', 'CONFIG')
        self.__logger.info('get video_record_enable :' + str(video_record_enable))
        if video_record_enable == 'yes':
            video_record = VideoRecord()
            video_record.start()
            self.__logger.info('start video_record ok !')
        update_task = UpdateTask()
        update_task.start()
        self.__logger.info('start update_task Ok!')
        interface_ros.init_ros_node()
        self.__logger.info('start init_ros_node Ok!')

        check_memory = get_value_by_key('check_memory', 'CONFIG')
        self.__logger.info('get check_memory :' + str(check_memory))
        if check_memory == 'yes':
            task_mem = Thread(target=get_mem_snap)
            task_mem.start()
        while True:
            time.sleep(1)
