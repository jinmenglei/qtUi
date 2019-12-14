# encoding: utf-8
# module ui.manager
# the manage ui logic
# no doc
from usher.ui.base_frame import BaseFrame
import time
import os

from base.U_log import get_logger
import base.U_util as Util
from base.U_dispatcher_qt import UDispatcher
from PyQt5 import QtCore, QtWidgets
import res.image_rc
from base.U_msg import UMsg
#
import tracemalloc
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
host_ui = ('0.0.0.0', 8889)


# mem test
def get_mem_snap():
    # test mem
    server = HTTPServer(host_ui, Resquest_ui)
    print("Starting server, listen at: %s:%s" % host_ui)
    task = Thread(target=server.serve_forever)
    task.start()
    global snap_finsh
    snap_finsh = False
    time.sleep(20)

    global snapshot_ui
    tracemalloc.start()
    snapshot_ui = tracemalloc.take_snapshot()
    snap_finsh = True


class Resquest_ui(BaseHTTPRequestHandler):
    def do_GET(self):
        if snap_finsh:
            snapshot2 = tracemalloc.take_snapshot()
            top_stats = snapshot2.compare_to(snapshot_ui, 'lineno')
            self.send_response(200)
            # self.send_header('Content-type', 'application/json')
            data = str(top_stats).replace('>, <', '> \r\n <')
        else:
            data = 'not init'
        self.wfile.write(bytes(data.encode('utf-8')))
# mem test


class UiManager(object):

    def __init__(self, manager_pipe):
        self.__module_name = 'ui_manager'
        print('ui_manager come in 57')
        self.__logger = get_logger(self.__module_name)
        print('ui_manager come in 59')
        self.dispatcher = None
        self.__frame = None
        self.__manager_pipe = manager_pipe
        self.__app = None
        self.widgets = None

    def start(self):

        self.__logger.info('begin to init pyqt5 app for this project!')
        # init widgets
        self.__app = QtWidgets.QApplication([])
        self.widgets = QtWidgets.QWidget()
        self.widgets.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.widgets.move(0, 0)
        self.widgets.resize(800, 480)

        print('ui_manager come in 76')

        if not os.path.isfile('./debug'):
            self.widgets.setCursor(QtCore.Qt.BlankCursor)

        self.dispatcher = UDispatcher(UMsg.ui_dispatcher, self.__manager_pipe)
        print('ui_manager come in 82')
        # init base_frame
        self.__frame = BaseFrame(self.widgets)

        print('ui_manager come in 86')

        # self.__change_page(0)

        # show main frame
        self.widgets.show()

        # test mem
        # Util.add_thread(target=get_mem_snap)

        self.__app.exec_()
        self.__logger.info('end!!!!!!')
        print('ui_manager come in 58')


if __name__ == '__main__':
    from base.U_dispatcher import Dispatcher
    dispatcher = Dispatcher()
    dispatcher.start()
    from usher.interface.manager import InterfaceManager
    IM = InterfaceManager()
    IM.start()
    import time
    time.sleep(1)
    manager = UiManager()
    manager.start()
    IM.init_ros_node()
    while True:
        # manager.test_show_box()
        time.sleep(2)
