from base.U_app import App
from base.U_log import get_logger
from usher.service.interface_ros import InterfaceRos
from usher.service.video_record import VideoRecord
from usher.service.Update_task import UpdateTask
from base.U_dispatcher import UDispatcher
import time

# test mem
import tracemalloc
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
host_server = ('0.0.0.0', 8890)

# mem test
def get_mem_snap():
    # test mem
    server = HTTPServer(host_server, Resquest_ui)
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


class Resquest_ui(BaseHTTPRequestHandler):
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


class ServiceManger(App):
    """
    服务的管理模块,显示和业务分开,其实是ros需要主线程,ui也是,所以
    目前包括:
    ros
    行车记录仪
    更新
    """
    def __init__(self, manager_pipe):
        self.module_name = 'service_manager'
        App.__init__(self, self.module_name)
        self.dispatcher = UDispatcher(self.msg_id.service_dispatcher, manager_pipe)
        self.__logger = get_logger(self.module_name)
        return

    def start(self):
        self.__logger.info('start service_manger!')
        interface_ros = InterfaceRos()
        interface_ros.start()
        self.__logger.info('start interface_ros ok')
        video_record = VideoRecord()
        video_record.start()
        self.__logger.info('start video_record ok !')
        update_task = UpdateTask()
        update_task.start()
        self.__logger.info('start update_task Ok!')
        interface_ros.init_ros_node()
        self.__logger.info('start init_ros_node Ok!')
        # task_mem = Thread(target=get_mem_snap)
        # task_mem.start()
        while True:
            time.sleep(1)
