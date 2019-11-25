from config.setting import *
import time
import base.U_util as Util
import base.U_app_qt as AppQt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from base.U_log import get_logger


class ModeMtPanel(AppQt.Q_App):
    """手动驾驶的panel"""
    def __init__(self, base_frame):
        self.module_name = 'mode_mt'
        self.logger = get_logger(self.module_name)
        AppQt.Q_App.__init__(self, self.module_name, base_frame, AppQt.QRect(0, 40, 800, 340))
        # frame init

        self.res_path = Util.get_res_path('mode_mt')
        self.list_msg_info = [['close', 'open', 'brush_req'], ['close', 'open', 'water_req'], ['forward', 'back'
            ,'direction_req']]

        self.list_mt_button_status = [Mt_button_off, Mt_button_off, Mt_button_forward]
        self.link_ros = False
        self.link_mcu = False

        tmp_list = list_label_mt_string
        for index in range(Mt_button_num):
            rect = tmp_list[index][list_label_point]
            name = tmp_list[index][list_label_info]
            AppQt.get_label_text(self, rect, True, name, 28, 'MicrosoftYaHei-Bold', '#000000')

        self.list_mt_button_bitmap = []
        self.list_mt_button = []
        tmp_list = list_button_mt_string
        for index in range(Mt_button_num):
            list_tmp = []
            bitmap = "border-image: url(:/mode_mt/mode_mt/" + str(tmp_list[index][Mt_button_off]) + ");"
            list_tmp.append(bitmap)
            bitmap = "border-image: url(:/mode_mt/mode_mt/" + str(tmp_list[index][Mt_button_on]) + ");"
            list_tmp.append(bitmap)
            self.list_mt_button_bitmap.append(list_tmp)

            rect = tmp_list[index][Mt_button_point]
            style_sheet = list_tmp[self.list_mt_button_status[index]]
            mt_button = AppQt.get_pushbutton(self, rect, style_sheet)

            mt_button.setObjectName(str(tmp_list[index][Mt_button_id]))
            mt_button.clicked.connect(lambda: self.on_click_mt_button(self.sender().objectName()))

            self.list_mt_button.append(mt_button)

        self.timer_show = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_show.timeout.connect(self.on_timer_show)

        self.timer_delay = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_delay.timeout.connect(self.on_timer_delay)

        self.__init_callback()

    def start(self):
        self.timer_show.start(1000)
        self.show_all_button()

    def stop(self):
        self.timer_show.stop()

    def __init_callback(self):
        self.subscribe_msg(self.msg_id.mode_mt_update_link_status, self.update_link_status_callback)
        self.subscribe_msg(self.msg_id.mode_mt_update_button_status, self.update_button_status_callback)

    def update_button_status_callback(self, data_dict):
        """
        {
            'msg_id' : 'mode_mt_update_button_status',
            'msg_data': {
                'brush_status': 'open', # close
                'water_status': 'open',
                'direction_status': 'forward' #back
            }
        }
        :param data_dict:
        :return:
        """
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None and isinstance(msg_data, dict):
            self.update_button_status_proc(msg_data)

    def update_button_status_proc(self, msg_data):
        if 'brush_status' in msg_data:
            if msg_data['brush_status'] == 'close':
                self.list_mt_button_status[Mt_brush_button] = Mt_button_off
            else:
                self.list_mt_button_status[Mt_brush_button] = Mt_button_on

        if 'water_status' in msg_data:
            if msg_data['water_status'] == 'close':
                self.list_mt_button_status[Mt_water_button] = Mt_button_off
            else:
                self.list_mt_button_status[Mt_water_button] = Mt_button_on

        if 'direction_status' in msg_data:
            if msg_data['direction_status'] == 'forward':
                self.list_mt_button_status[Mt_direction_button] = Mt_button_forward
            else:
                self.list_mt_button_status[Mt_direction_button] = Mt_button_back

    def update_link_status_callback(self, data_dict):
        """
        {
            'msg_id' : 'mode_mt_update_link_status',
            'msg_data': {
                'link_ros': False,
                'link_mcu': False
            }
        }
        :param data_dict:
        :return:
        """
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None and isinstance(msg_data, dict):
            self.update_link_status_proc(msg_data)

    def update_link_status_proc(self, msg_data):
        link_ros = msg_data.get('link_ros')
        link_mcu = msg_data.get('link_mcu')
        if link_ros is not None and isinstance(link_ros, bool):
            self.link_ros = link_ros

        if link_mcu is not None and isinstance(link_mcu, bool):
            self.link_mcu = link_mcu

    def on_timer_delay(self):
        self.timer_delay.stop()

    def ui_control_ros(self, index):
        tmp_list = self.list_msg_info[index]
        msg_id_index = 2
        tmp_status = self.list_mt_button_status[index]
        msg_data = {'msg_id': tmp_list[msg_id_index], 'msg_type': 'control',
                    'msg_data': tmp_list[tmp_status]}
        self.send_msg_out(msg_data)

    def on_click_mt_button(self, index):
        """水位,刷盘,方向控制"""
        button_index = int(index) - Mt_button_id_delta
        if button_index not in range(Mt_button_num):
            return
        # self.stop()
        if self.timer_delay.isActive():
            return
        if not self.link_ros or not self.link_mcu:
            self.logger.info('show box ' + str(show_box_loss))
            self.show_box(show_box_loss, '')
            return

        list_status = self.list_mt_button_status
        list_button = self.list_mt_button
        list_bitmap = self.list_mt_button_bitmap

        # print(self.list_mt_button_status)

        self.timer_delay.start(200)
        list_status[button_index] = list_status[button_index] ^ 1
        # print(self.list_mt_button_status)
        list_button[button_index].setStyleSheet(list_bitmap[button_index][list_status[button_index]])

        self.ui_control_ros(button_index)
        # self.start()

    def show_all_button(self):
        list_status = self.list_mt_button_status
        list_button = self.list_mt_button
        list_bitmap = self.list_mt_button_bitmap

        for index in range(Mt_button_num):
            list_button[index].setStyleSheet(list_bitmap[index][list_status[index]])

    def on_timer_show(self):
        """标题栏刷新定时器"""
        if not self.timer_delay.isActive() and self.isVisible():
            self.show_all_button()
