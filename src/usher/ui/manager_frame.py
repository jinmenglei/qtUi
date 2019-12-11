# encoding: utf-8
# module ui.manager
# the manage ui logic
# no doc

from usher.ui.mode_mt import ModeMtPanel
from usher.ui.mode_author import ModeAuthorPanel
from usher.ui.mode_check import ModeCheckPanel
from usher.ui.mode_map_select import ModeMapSelectPanel
from usher.ui.mode_working import ModeWorkingPanel
from usher.ui.mode_show_box import ModeShowBox
from usher.ui.mode_update import ModeUpdate
from usher.ui.mode_start import ModeStart
import time

import config.setting as setting
import base.U_app_qt as AppQt
from base.U_log import get_logger
import base.U_util as Util
from PyQt5 import QtCore, QtWidgets


module_relations = {
    setting.Page_mt_mode: ModeMtPanel,
    setting.Page_author: ModeAuthorPanel,
    setting.Page_check: ModeCheckPanel,
    setting.Page_map_select: ModeMapSelectPanel,
    setting.Page_working: ModeWorkingPanel,
    setting.Page_Update: ModeUpdate,
}


class ManagerFrame(AppQt.Q_App):

    def __init__(self, base_frame):
        self.__frame = base_frame
        self.__module_name = 'manager_frame'
        AppQt.Q_App.__init__(self, self.__module_name, parent=base_frame, geometry=QtCore.QRect(0, 40, 800, 340))

        self.__logger = get_logger(self.__module_name)

        self.__default_page = setting.Page_mt_mode
        self.robot_status = 'mt'
        self.show_box_panel = None  # type: AppQt.Q_App
        self.start_panel = None  # type: AppQt.Q_App
        self.page_stack = None  # type: QtWidgets.QStackedWidget

        self.__init_callback()

        self.__run()
        # print(self.page_stack)

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
        # self.__logger.info('##########' + str(data_dict))
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
            self.show_box_panel = ModeShowBox(self.__frame)
        self.show_box_panel.show()
        self.show_box_panel.show_box_tip(index, tip)

    def __change_page(self, index):
        self.__logger.info('change panel to index : ' + str(index))

        if self.start_panel.isVisible():
            self.start_panel.hide()

        if index in range(setting.Page_num - 1):
            if self.show_box_panel.isVisible():
                self.show_box_panel.hide()
            self.page_stack.setCurrentIndex(index)

        if not self.page_stack.isVisible():
            self.page_stack.show()

        self.__update_button_status(index)

    def __update_button_status(self, index):
        msg_data = {'page_mode': index}
        self.send_msg_dispatcher(self.msg_id.base_frame_update_button_status, msg_data)

    def init_all_page(self):
        self.start_panel = ModeStart(self.__frame)
        self.start_panel.show()
        for index in range(setting.Page_num):
            tmp_frame = module_relations[index](self)
            self.page_stack.addWidget(tmp_frame)

        self.page_stack.hide()

        self.show_box_panel = ModeShowBox(self.__frame)
        self.show_box_panel.hide()

        self.send_ui_start_success()

    def send_ui_start_success(self):
        msg_data = {'index': setting.start_ui, 'status': True}
        self.send_msg_dispatcher(self.msg_id.mode_start_status, msg_data)

    def __run(self):
        self.__logger.info('begin to init manager_frame frame for this project!')

        # init stackWidget
        self.page_stack = QtWidgets.QStackedWidget(self)
        self.page_stack.setFixedSize(800, 340)
        # init all frame
        self.init_all_page()

        # show default page
        # self.__change_page(self.__default_page)

        self.__logger.info('end to init manager_frame frame for this project!')
