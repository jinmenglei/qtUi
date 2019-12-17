from PyQt5.QtWidgets import QPushButton

from config.setting import *
import time
import base.U_util as Util
import base.U_app_qt as AppQt
from base.U_log import get_logger
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import os


class ModeMapSelectPanel(AppQt.Q_App):
    """手动驾驶的panel"""
    start_timer_show_signal = pyqtSignal()
    stop_timer_show_signal = pyqtSignal()

    def __init__(self, base_frame):
        self.module_name = 'mode_map_select'
        self.logger = get_logger(self.module_name)
        AppQt.Q_App.__init__(self, self.module_name, base_frame)
        self.show_callback = self.start
        self.hide_callback = self.stop

        self.res_path = Util.get_res_path(self.module_name)

        # self.get_map_num()
        style_sheet = 'QPushButton{border-image: url(:/mode_map_select/mode_map_select/左-亮.png)}' + \
                      'QPushButton:pressed{border-image: url(:/mode_map_select/mode_map_select/左-灰.png)}'
        self.m_button_left = AppQt.get_pushbutton(self, QRect(20, 140, 58, 58), style_sheet)

        # self.get_map_num()
        style_sheet = 'QPushButton{border-image: url(:/mode_map_select/mode_map_select/右-亮.png)}' + \
                      'QPushButton:pressed{border-image: url(:/mode_map_select/mode_map_select/右-灰.png)}'
        self.m_button_right = AppQt.get_pushbutton(self, QRect(720, 140, 58, 58), style_sheet)

        self.map_frame = AppQt.get_sub_frame(self, QRect(100, 0, 600, 340))

        self.list_map_button = []
        self.list_map_frame = []
        self.list_map_label = []
        self.list_map = []

        self.timer_show = QtCore.QTimer()  # 创建定时器
        self.timer_show.timeout.connect(lambda: self.on_timer_show())  # 绑定一个定时器事件

    def get_map_num(self):

        list_map = Util.get_map_num()

        self.m_button_left.hide()
        self.m_button_right.hide()

        if len(list_map) == 0:
            self.show_box(show_box_need_build_map, '')
        else:
            if list_map == self.list_map:
                pass
            else:
                self.list_map = list_map
                for button in self.list_map_button:
                    button.disconnect()
                    button.destroy()
                self.list_map_button.clear()
                for frame in self.list_map_frame:
                    frame.destroy()
                self.list_map_frame.clear()

                for label in self.list_map_label:
                    label.destroy()
                self.list_map_label.clear()

                position_cnt = 0
                for map_detail in list_map:
                    if position_cnt % 2 == 0:
                        rect_back = QRect(0 + (126 + 32) * int(position_cnt / 2), 7, 126, 126)
                        rect_title = QRect(0 + (126 + 32) * int(position_cnt / 2), 139, 126, 26)
                    else:
                        rect_back = QRect(0 + (126 + 32) * int(position_cnt / 2), 175, 126, 126)
                        rect_title = QRect(0 + (126 + 32) * int(position_cnt / 2), 307, 126, 26)

                    frame = AppQt.get_sub_frame(self.map_frame, rect_back, 'background-color: #FFFFFF;')
                    frame.show()
                    png_path = map_detail.get('png')
                    name = map_detail.get('name')
                    style_sheet = 'QPushButton{border-image: url(' + png_path + ')}'

                    rect = AppQt.QRect(3, 3, 120, 120)
                    map_button = AppQt.get_pushbutton(frame, rect, style_sheet)  # type: QPushButton
                    map_button.setObjectName(str(position_cnt + Map_button_id_delta))
                    map_button.show()

                    map_button.clicked.connect(lambda: self.on_click_map_button(int(self.sender().objectName())))

                    self.list_map_button.append(map_button)

                    map_label = AppQt.get_label_text(self.map_frame, rect_title, False, name, 26)
                    map_label.show()

                    self.list_map_label.append(map_label)
                    position_cnt += 1
                self.map_frame.show()

        pass

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
        self.get_map_num()
        self.timer_show.start(1000)

    def stop(self):
        self.timer_show.stop()

    def on_timer_show(self):
        """标题栏刷新定时器"""
        pass


