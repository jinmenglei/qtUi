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
from base.U_app import App
from base.U_log import get_logger
import base.U_util as Util
import time
from base.U_dispatcher import UDispatcher
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
# from PyQt5.QtWidgets.
import image_rc

module_relations = {
    Page_mt_mode: ModeMtPanel,
    Page_author: ModeAuthorPanel,
    Page_check: ModeCheckPanel,
    Page_map_select: ModeMapSelectPanel,
    Page_working: ModeWorkingPanel,
    Page_show_box: ModeShowBox,
    Page_Update: ModeUpdate,
}


class UiManager(QObject, App):
    def __init__(self, manager_pipe):
        self.__module_name = 'ui_manager'

        App.__init__(self, self.__module_name)
        # QtWidgets.QWidget.__init__(self, None)
        self.__logger = get_logger(self.__module_name)
        self.ui_dispatcher = UDispatcher(self.msg_id.ui_dispatcher, manager_pipe)
        self.__old_panel = None
        self.__frame = None
        self.__app = None
        self.__default_page = Page_mt_mode
        self.robot_status = 'mt'

        self.page_dict = {}
        self.__init()

    def __init(self):
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
        self.__logger.info('destory box ')
        if self.page_dict[Page_show_box] is None:
            self.page_dict[Page_show_box] = module_relations[Page_show_box](self.__frame)
        print(self.page_dict)
        self.page_dict[Page_show_box].hide()

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
        if self.page_dict[Page_show_box] is None:
            self.page_dict[Page_show_box] = module_relations[Page_show_box](self.__frame)
        self.page_dict[Page_show_box].show()
        self.page_dict[Page_show_box].show_box_tip(index, tip)

    def test_ui_stable(self):
        count = 0
        time.sleep(5)
        while True:
            time.sleep(1)
            self.__change_page(Page_mt_mode)
            time.sleep(1)
            self.__change_page(Page_author)
            self.__logger.info('change conut : ' + str(count))
            count += 1

    def __change_page(self, index):
        self.__logger.info('change panel to index : ' + str(index))

        for index_page in range(Page_num):
            if index_page == index:
                self.page_dict[index_page].show()
                self.page_dict[index_page].start()
            else:
                self.page_dict[index_page].hide()
                self.page_dict[index_page].stop()
        # self.__old_panel = module_relations[index](self.__frame)
        # self.__old_panel.start()
        # self.__old_panel.Show(True)

        self.__update_button_status(index)
        pass

    def __update_button_status(self, index):
        msg_data = {'page_mode': index}
        self.send_msg_dispatcher(self.msg_id.base_frame_update_button_status, msg_data)

    def start(self):
        # task = Thread(target=self.__run)
        # task.start()
        self.__run()

    def init_all_page(self):
        for index in range(Page_num):
            self.page_dict[index] = module_relations[index](self.__frame)
            self.page_dict[index].hide()

    def __run(self):
        """__run__ is parent function dont rewrite"""
        self.__logger.info('begin to init pyqt5 app for this project!')
        # init
        self.__app = QtWidgets.QApplication([])
        self.widgets = QtWidgets.QWidget()
        self.widgets.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.widgets.move(0, 0)
        self.widgets.resize(800, 480)
        self.__frame = BaseFrame(self.widgets)
        self.__frame.start()
        self.init_all_page()

        # add panel here
        # self.__change_page(self.__default_page)
        self.__change_page(6)


        # show main frame
        self.widgets.show()
        # Util.add_thread(target=self.test_ui_stable)
        try:
            self.__app.exec_()
            print('end')
        except Exception as e:
            print(str(e))
            time.sleep(1)

    # def on_timer_delay(self,event):
    #     if event:
    #         pass
    #
    #     if self.old_page_index != self.page_index:
    #         self.__change_page(self.page_index)
    #
    #     elif self.show_box_flag:
    #         if self.old_show_box_index != self.show_box_index or self.old_show_box_tip != self.show_box_tip:
    #             self.__show_box(self.show_box_index, self.show_box_tip)
    #
    #     elif not self.show_box_flag and self.page_dict[Page_show_box].IsShownOnScreen():
    #         if self.page_dict[Page_show_box] is not None:
    #             self.page_dict[Page_show_box].stop()
    #             self.page_dict[Page_show_box].Show(False)
    #             self.old_show_box_index = None
    #             self.old_show_box_tip = None




if __name__ == '__main__':
    from service.dispatcher import Dispatcher
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
