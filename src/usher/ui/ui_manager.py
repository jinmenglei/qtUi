# encoding: utf-8
# module ui.manager
# the manage ui logic
# no doc

from usher.ui.base_frame import BaseFrame
from usher.ui.mode_mt import ModeMtPanel
from usher.ui.mode_author import ModeAuthorPanel
from usher.ui.mode_check import ModeCheckPanel
from usher.ui.mode_map_select import ModeMapSelectPanel
from usher.ui.mode_working import ModeWorkingPanel
from usher.ui.mode_show_box import ModeShowBox
from usher.ui.mode_update import ModeUpdate

from config.setting import *
from base.U_app_qt import App, App_Qobject
from base.U_log import get_logger
import base.U_util as Util
from base.U_dispatcher import UDispatcher
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
import res.image_rc
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


module_relations = {
    Page_mt_mode: ModeMtPanel,
    Page_author: ModeAuthorPanel,
    Page_check: ModeCheckPanel,
    Page_map_select: ModeMapSelectPanel,
    Page_working: ModeWorkingPanel,
    Page_show_box: ModeShowBox,
    Page_Update: ModeUpdate,
}


class UiManager(App_Qobject):
    def __init__(self, manager_pipe):
        self.__module_name = 'ui_manager'
        self.__app = QtWidgets.QApplication([])
        App_Qobject.__init__(self, self.__module_name)

        self.__logger = get_logger(self.__module_name)
        self.ui_dispatcher = UDispatcher(self.msg_id.ui_dispatcher, manager_pipe)
        self.__frame = None
        self.__default_page = Page_mt_mode
        self.robot_status = 'mt'
        self.show_box_panel = None
        self.page_stack = None

        self.__init_callback()

    def __init_callback(self):
        self.subscribe_msg(self.msg_id.ui_manager_show_box, self.__show_box_callback)
        self.subscribe_msg(self.msg_id.ui_manager_change_page, self.__change_page_callback)
        self.subscribe_msg(self.msg_id.ui_manager_robot_status_notify, self.__robot_status_callback)
        self.subscribe_msg(self.msg_id.ui_manager_destroy_show_box, self.__destroy_show_box_callback)

    def __destroy_show_box_callback(self, data_dict):
        """
        {
            'msg_id': 'ui_manager_robot_status_notify',
            'msg_data':{
                'robot_status': 'mt'
            }
        }
        :param data_dict:
        :return:
        """
        self.__logger.info('destroy box ')
        # if self.page_dict[Page_show_box] is None:
        #     self.page_dict[Page_show_box] = module_relations[Page_show_box](self.__frame)
        # print(self.page_dict)
        # self.page_dict[Page_show_box].hide()

    def __robot_status_callback(self, data_dict):
        """
        {
            'msg_id': 'ui_manager_robot_status_notify',
            'msg_data':{
                'robot_status': 'mt'
            }
        }
        :param data_dict:
        :return:
        """
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None and isinstance(msg_data, dict):
            status = msg_data.get('robot_status')
            if status == 'mt' or status == 'at':
                self.robot_status = status

    def __show_box_callback(self, data_dict):
        """
        data_dict =
        {
            'msg_id' : 'ui_manager_show_box',
            'msg_data' : {
                'index' : 1 ,
                'tip' : 'this a tip for show box'
            }
        }
        """
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None:
            index, tip = Util.get_index_tip_msg_data(msg_data)
            if index is not None:
                self.__show_box(index, tip)

    def __change_page_callback(self, data_dict):
        """
        data_dict =
        {
            'msg_id' : 'ui_manager_change_page',
            'msg_data' : {
                'page_mode',1
            }
        }
        """
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None and isinstance(msg_data, dict):
            page_mode = msg_data.get('page_mode')
            if page_mode is not None and isinstance(page_mode, int):
                self.__logger.info('change mode ' + str(page_mode))
                self.__change_page(page_mode)

    def __show_box(self, index, tip=''):
        self.__logger.info('show box index :' + str(index) + '--tip : ' + str(tip))
        if self.show_box_panel is None:
            self.show_box_panel = module_relations[Page_show_box](self.__frame)
        self.show_box_panel.show()
        self.show_box_panel.show_box_tip(index, tip)

    def test_ui_stable(self):
        count = 0
        time.sleep(5)
        index = 0
        while True:
            time.sleep(1)
            if index in range(Page_num):
                self.mode_dispatcher(index)
                index += 1
            else:
                index = 0
            self.__logger.info('change conut : ' + str(count))
            count += 1

    def __change_page(self, index):
        self.__logger.info('change panel to index : ' + str(index))

        if index in range(Page_num - 1):
            self.page_stack.setCurrentIndex(index)

        self.__update_button_status(index)

    def __update_button_status(self, index):
        msg_data = {'page_mode': index}
        self.send_msg_dispatcher(self.msg_id.base_frame_update_button_status, msg_data)

    def start(self):
        self.__run()

    def init_all_page(self):
        for index in range(Page_num - 1):
            tmp_frame = module_relations[index](self.__frame)
            self.page_stack.addWidget(tmp_frame)

        self.show_box_panel = module_relations[Page_show_box](self.__frame)
        self.show_box_panel.hide()

    def __run(self):
        self.__logger.info('begin to init pyqt5 app for this project!')
        # init widgets
        self.widgets = QtWidgets.QWidget()
        self.widgets.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.widgets.move(0, 0)
        self.widgets.resize(800, 480)
        # init base_frame
        self.__frame = BaseFrame(self.widgets)
        # init stackWidget
        self.page_stack = QtWidgets.QStackedWidget(self.__frame)
        self.page_stack.setGeometry(0, 40, 800, 340)
        # init all frame
        self.init_all_page()

        # show default page
        self.__change_page(self.__default_page)
        # self.__change_page(0)

        # show main frame
        self.widgets.show()
        # test auto
        # Util.add_thread(target=self.test_ui_stable)

        # test mem
        # Util.add_thread(target=get_mem_snap)

        self.__app.exec_()
        print('end')


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
