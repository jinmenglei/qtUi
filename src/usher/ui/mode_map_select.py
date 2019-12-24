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
        self.map_frame.show()

        self.list_map_button = []
        self.list_map_frame = []
        self.list_map_label = []
        self.list_map = []

        self.timer_show = QtCore.QTimer()  # 创建定时器
        self.timer_show.timeout.connect(lambda: self.on_timer_show())  # 绑定一个定时器事件
        self.timer_update_map = QtCore.QTimer()  # 创建定时器
        self.timer_update_map.timeout.connect(lambda: self.on_timer_update_map())  # 绑定一个定时器事件
        self.position_cnt = 0

        self.__init_callback()

    def __init_callback(self):
        pass

    def do_update_map(self):
        self.timer_update_map.stop()
        list_map_len = len(self.list_map)
        pos = self.get_map_qrect(list_map_len)

        if self.position_cnt >= len(self.list_map):
            return
        map_detail = self.list_map[self.position_cnt]

        rect_back, rect_title = self.get_qrect(pos, list_map_len, self.position_cnt)

        frame = AppQt.get_sub_frame(self.map_frame, rect_back, 'background-color: #FFFFFF;')
        frame.show()

        self.list_map_frame.append(frame)
        png_path = map_detail.get('png')
        style_sheet = 'QPushButton{border-image: url(' + png_path + ')}'

        rect = AppQt.QRect(3, 3, pos['map_weight'] - 2 * 3, pos['map_weight'] - 2 * 3)
        map_button = AppQt.get_pushbutton(frame, rect, style_sheet)  # type: QPushButton
        map_button.setObjectName(str(self.position_cnt + Map_button_id_delta))
        map_button.show()

        map_button.clicked.connect(lambda: self.on_click_map_button(int(self.sender().objectName())))

        self.list_map_button.append(map_button)

        name = map_detail.get('name')
        map_label = AppQt.get_label_text(self.map_frame, rect_title, False, name, 26)
        map_label.show()

        self.list_map_label.append(map_label)
        self.timer_update_map.start(20)
        pass

    def on_timer_update_map(self):
        self.do_update_map()
        self.position_cnt += 1

    def clear_all(self):
        for button in self.list_map_button:
            button.disconnect()
            button.deleteLater()
        self.list_map_button.clear()

        for label in self.list_map_label:
            label.deleteLater()
        self.list_map_label.clear()

        for frame in self.list_map_frame:
            frame.deleteLater()
        self.list_map_frame.clear()

    def get_map_qrect(self, list_map_len):
        position = {
            'x_start_top': 0,
            'x_start_tail': 0,
            'x_delta': 126 + 32,
            'y_button_top': 7,
            'y_label_top': 139,
            'y_button_tail': 175,
            'y_label_tail': 307,
            'map_weight':126
        }
        if list_map_len > 7:
            pass
        elif list_map_len == 7:
            position['x_start_tail'] = 79
        elif list_map_len == 6:
            position['x_start_top'] = position['x_start_tail'] = 79
        elif list_map_len == 5:
            position['x_start_top'] = 79
            position['x_start_tail'] = 158
        elif list_map_len == 4:
            position['y_button_top'] = 91
            position['y_label_top'] = 91 + 126 + 6
        elif list_map_len == 3:
            position['map_weight'] = 180
            position['y_button_top'] = 64
            position['y_label_top'] = 64 + 180 + 6
            position['x_delta'] = 180 + 30
        elif list_map_len == 2:
            position['map_weight'] = 280
            position['y_button_top'] = 14
            position['y_label_top'] = 14 + 280 + 6
            position['x_delta'] = 280 + 40
        else:
            position['map_weight'] = 280
            position['y_button_top'] = 14
            position['y_label_top'] = 14 + 280 + 6
            position['x_start_top'] = 160
        self.logger.info('get rect: ' + str(position))
        return position

    def get_qrect(self, pos, list_map_len, position_cnt):
        if list_map_len <= 4:
            rect_back = QRect(pos['x_start_top'] + pos['x_delta'] * position_cnt, pos['y_button_top'],
                              pos['map_weight'], pos['map_weight'])
            rect_title = QRect(pos['x_start_top'] + pos['x_delta'] * position_cnt - 10, pos['y_label_top'],
                               pos['map_weight'] + 20, 26)
        else:
            if position_cnt % 2 == 0:
                rect_back = QRect(pos['x_start_top'] + pos['x_delta'] * int(position_cnt / 2),
                                  pos['y_button_top'], pos['map_weight'], pos['map_weight'])
                rect_title = QRect(pos['x_start_top'] + pos['x_delta'] * int(position_cnt / 2) - 10,
                                   pos['y_label_top'], pos['map_weight'] + 20, 26)
            else:
                rect_back = QRect(pos['x_start_tail'] + pos['x_delta'] * int(position_cnt / 2),
                                  pos['y_button_tail'], pos['map_weight'], pos['map_weight'])
                rect_title = QRect(pos['x_start_tail'] + pos['x_delta'] * int(position_cnt / 2) - 10,
                                   pos['y_label_tail'], pos['map_weight'] + 20, 26)
        self.logger.info('get rect back : ' + str(rect_back))
        self.logger.info('get rect title : ' + str(rect_title))
        return rect_back, rect_title

    def get_map_num(self):

        list_map = Util.get_map_num()

        self.m_button_left.hide()
        self.m_button_right.hide()
        list_map_len = len(list_map)

        if list_map_len == 0:
            self.timer_update_map.stop()
            self.show_box(show_box_need_build_map, '')
        else:
            if list_map == self.list_map:
                self.timer_update_map.stop()
                return
            else:
                self.list_map = list_map

                self.clear_all()

                self.position_cnt = 0

                self.timer_update_map.start(50)


        # if list_map_len > 8:
        #     self.m_button_right.show()
        pass

    def on_click_map_button(self, index):
        """选择地图按钮处理事件"""
        self.logger.info('click ' + str(index) + 'map')
        button_index = index - Map_button_id_delta

        if 0 <= button_index < len(self.list_map):
            if Util.change_wp_file(self.list_map[button_index].get('wp')) and \
                    Util.change_pcd_file(self.list_map[button_index].get('pcd')):
                map_select_path = self.list_map[button_index].get('png')
                map_select_name = self.list_map[button_index].get('name')
                self.show_box(show_box_map_select, '【' + map_select_name + '】?')
                data_dict = {'map_path': map_select_path, 'map_name': map_select_name}
                self.send_msg_dispatcher(self.msg_id.mode_working_show_map, data_dict)
            else:
                self.show_box(show_box_launch_fail, '')

    def start(self):
        self.get_map_num()
        self.timer_show.start(1000)

    def stop(self):
        self.timer_show.stop()
        self.timer_update_map.stop()

    def on_timer_show(self):
        """标题栏刷新定时器"""
        pass


