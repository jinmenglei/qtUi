from PyQt5.QtWidgets import QPushButton

from config.setting import *
import time
import base.U_util as Util
import base.U_app_qt
from base.U_log import get_logger
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class ModeMapSelectPanel(base.U_app_qt.Q_App):
    """手动驾驶的panel"""
    start_timer_show_signal = pyqtSignal()
    stop_timer_show_signal = pyqtSignal()

    def __init__(self, base_frame):
        self.module_name = 'mode_map_select'
        self.logger = get_logger(self.module_name)
        base.U_app_qt.Q_App.__init__(self, self.module_name, base_frame, base.U_app_qt.QRect(0, 40, 800, 340))
        self.show_callback = self.start
        self.hide_callback = self.stop

        self.res_path = Util.get_res_path(self.module_name)

        self.list_map_button = []
        self.list_map_label = []
        for index in range(Map_select_num):
            rect = list_button_map_string[index][Map_back_point]
            label_frame = base.U_app_qt.get_sub_frame(self, rect, 'background-color: #FFFFFF;')

            rect = base.U_app_qt.QRect(3, 3, 120, 120)
            style_sheet = "border-image: url(:/mode_map_select/mode_map_select/" + \
                            str(list_button_map_string[index][Map_button_path]) + ");"

            map_button = base.U_app_qt.get_pushbutton(label_frame, rect, style_sheet)  # type: QPushButton

            button_id = list_button_map_string[index][Map_button_id]
            map_button.setObjectName(str(button_id))

            map_button.clicked.connect(lambda: self.on_click_map_button(int(self.sender().objectName())))

            self.list_map_button.append(map_button)

            rect = list_button_map_string[index][Map_label_point]
            name = list_button_map_string[index][Map_label_string]
            map_label = base.U_app_qt.get_label_text(self, rect, False, name, 26)

            self.list_map_label.append(map_label)

            self.timer_show = QtCore.QTimer()  # 创建定时器
            self.timer_show.timeout.connect(lambda: self.on_timer_show())  # 绑定一个定时器事件

    def on_click_map_button(self, index):
        """选择地图按钮处理事件"""
        self.logger.info('click ' + str(index) + 'map')
        button_index = index - Map_button_id_delta

        if 0 <= button_index < Map_select_num:

            map_select_path = self.res_path + list_button_map_string[button_index][Map_button_path]
            map_select_name = list_button_map_string[button_index][Map_label_string]
            self.show_box(show_box_map_select, '【' + map_select_name + '】?')
            data_dict = {'map_path': map_select_path, 'map_name': map_select_name}
            self.send_msg_dispatcher(self.msg_id.mode_working_show_map, data_dict)

    def start(self):
        self.timer_show.start(1000)

    def stop(self):
        self.timer_show.stop()

    def on_timer_show(self):
        """标题栏刷新定时器"""
        pass


