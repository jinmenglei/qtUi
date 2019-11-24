# encoding: utf-8
# module ui.frame
# the basic class of ui
# no doc

import time
from config.setting import *
import base.U_util as Util
from base.U_app_qt import Q_App
from PyQt5 import  QtCore, QtGui, QtWidgets
import res.image_rc
from base.U_log import get_logger


class BaseFrame(Q_App):
    """whole ui base class"""

    def __init__(self, parent):
        self.module_name = 'base_frame'
        # init frame
        Q_App.__init__(self, self.module_name, parent=parent)

        # init variable
        self.res_path = Util.get_res_path('frame')
        self.logger = get_logger(self.module_name)

        self.one_second_cnt = 0
        # home
        self.battery_count = 88
        self.water_count = 88
        self.odom_count = 1.2
        self.line_speed = 0
        self.received_time = 0

        self.link_4G = True
        self.link_ros = False
        self.link_mcu = False

        self.list_mt_button_status = [Mt_button_off, Mt_button_off, Mt_button_forward]

        # init self
        self.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.setStyleSheet("background-color: rgb(214, 213, 214);")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setLineWidth(0)
        self.show()
        # title panel init
        self.title_panel = QtWidgets.QFrame(self)
        self.title_panel.setGeometry(QtCore.QRect(0, 0, 800, 40))
        self.title_panel.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.title_panel.setFrameShape(QtWidgets.QFrame.NoFrame)


        # tail panel init
        self.tail_panel = QtWidgets.QFrame(self)
        self.tail_panel.setGeometry(QtCore.QRect(0, 380, 800, 100))
        self.tail_panel.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.tail_panel.setFrameShape(QtWidgets.QFrame.NoFrame)

        # init title 4G
        self.m_bitmap_4G = QtWidgets.QLabel(self.title_panel)
        self.m_bitmap_4G.setGeometry(QtCore.QRect(13, 12, 28, 17))
        self.m_bitmap_4G.setText("")
        self.m_bitmap_4G.setPixmap(QtGui.QPixmap(":/frame/frame/信号4.png"))

        # init title battery
        self.m_bitmap_battery = QtWidgets.QLabel(self.title_panel)
        self.m_bitmap_battery.setGeometry(QtCore.QRect(745, 11, 43, 18))
        self.m_bitmap_battery.setText("")
        self.m_bitmap_battery.setPixmap(QtGui.QPixmap(":/frame/frame/电池1.png"))

        # init tail water percent
        self.m_bitmap_water = QtWidgets.QLabel(self.tail_panel)
        self.m_bitmap_water.setGeometry(QtCore.QRect(47, 26, 40, 54))
        self.m_bitmap_water.setText("")
        self.m_bitmap_water.setPixmap(QtGui.QPixmap(":/frame/frame/水量.png"))

        # init tail odom
        self.m_bitmap_odom = QtWidgets.QLabel(self.tail_panel)
        self.m_bitmap_odom.setGeometry(QtCore.QRect(597, 26, 44, 54))
        self.m_bitmap_odom.setText("")
        self.m_bitmap_odom.setPixmap(QtGui.QPixmap(":/frame/frame/lichen.png"))

        # 剩下的label 批量处理,省地方
        self.m_title_label_list = []
        tmp_list = list_title_string
        for index in range(len(tmp_list)):
            # Label初始化
            title_label = QtWidgets.QLabel(self.title_panel)
            title_label.setGeometry(tmp_list[index][Title_index_point])
            font = QtGui.QFont()
            font.setFamily("MicrosoftYaHei")
            font.setPointSize(tmp_list[index][Title_index_font_size])
            font.setBold(True)
            font.setItalic(False)
            font.setWeight(50)
            title_label.setFont(font)
            title_label.setStyleSheet("color: rgb(0, 0, 0);")
            title_label.setText(tmp_list[index][Title_index_name])
            title_label.setAutoFillBackground(True)
            self.m_title_label_list.append(title_label)

        # 剩下的label 批量处理,省地方
        self.m_tail_label_list = []
        tmp_list = list_tail_string
        for index in range(len(tmp_list)):
            title_label = QtWidgets.QLabel(self.tail_panel)
            title_label.setGeometry(tmp_list[index][Title_index_point])
            font = QtGui.QFont()
            font.setFamily("MicrosoftYaHei")
            font.setPointSize(tmp_list[index][Title_index_font_size])
            font.setBold(True)
            font.setItalic(False)
            font.setWeight(50)
            title_label.setFont(font)
            title_label.setStyleSheet("color: rgb(0, 0, 0);")
            title_label.setText(tmp_list[index][Title_index_name])
            self.m_tail_label_list.append(title_label)

        # init at or mt button

        self.m_bpButtonAt_mini = QtWidgets.QPushButton(self.tail_panel)
        self.m_bpButtonAt_mini.setGeometry(QtCore.QRect(235, 0, 331, 100))
        self.m_bpButtonAt_mini.setStyleSheet("border-image: url(:/frame/frame/切换到 自动驾驶.png);")
        self.m_bpButtonAt_mini.setText("")
        self.m_bpButtonAt_mini.hide()

        self.m_bpButtonMt_mini = QtWidgets.QPushButton(self.tail_panel)
        self.m_bpButtonMt_mini.setGeometry(QtCore.QRect(235, 0, 331, 100))
        self.m_bpButtonMt_mini.setStyleSheet("border-image: url(:/frame/frame/切换到 手动驾驶.png);")
        self.m_bpButtonMt_mini.setText("")
        self.m_bpButtonMt_mini.hide()


        # create timer for title and tail update
        self.timer_show = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_show.timeout.connect(self.on_timer_show)
        QtCore.QMetaObject.connectSlotsByName(parent)

        self.__init_callback()

    def __init_callback(self):
        """
        init callback
        :return:
        """
        self.subscribe_msg(self.msg_id.base_frame_info_notify, self.info_notify_callback)
        self.subscribe_msg(self.msg_id.base_frame_set_button_enable, self.set_button_enable_callback)
        self.subscribe_msg(self.msg_id.base_frame_update_link_status, self.update_link_status_callback)
        self.subscribe_msg(self.msg_id.base_frame_update_button_status, self.update_button_status_callback)

    def update_button_status_callback(self, data_dict):
        """
        {
            'msg_id' : 'base_frame_update_button_status',
            'msg_data': {
                'page_mode': 1
            }
        }
        :param data_dict:
        :return:
        """

        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None and isinstance(msg_data, dict):
            self.logger.info('get_status :' + str(data_dict))
            self.update_button_status_proc(msg_data)

    def update_button_status_proc(self, msg_data):
        """
        :param msg_data:
        :return:
        """
        page_mode = msg_data.get('page_mode')
        if page_mode is not None and isinstance(page_mode, int):
            self.show_mt_at(page_mode)

    def update_link_status_callback(self, data_dict):
        """
        {
            'msg_id' : 'base_frame_update_link_status',
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

    def set_button_enable_callback(self, data_dict):
        """
        {
            'msg_id': 'base_frame_set_button_enable',
            'msg_data':{
                'button_enable': False
            }
        }
        :param data_dict:
        :return:
        """
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None and isinstance(msg_data, dict):
            self.set_button_enable_msg_data_proc(msg_data)

    def set_button_enable_msg_data_proc(self, msg_data):
        """
        :param msg_data:
        :return:
        """
        enable = msg_data.get('button_enable')
        if enable is not None and isinstance(enable, bool):
            self.set_button_enable(enable)

    def info_notify_callback(self, data_dict):
        """
        {
            'msg_id': 'base_frame_info_notify',
            'msg_data': {
                'voltage_percent': 88,
                'yewei2_percent': 88,
                'Position_X': '0.3',
                'Position_Y': '0.3'
            }
        }
        :param data_dict:
        :return:
        """
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None and isinstance(msg_data, dict):
            self.info_notify_msg_data_proc(msg_data)

    def info_notify_msg_data_proc(self, msg_data):
        """
        :param msg_data:
        :return:
        """
        if self.received_time is not 0:
            delta_time = time.time() - self.received_time
            self.odom_count += (delta_time * self.line_speed) / 1000

        self.received_time = time.time()

        if 'voltage_percent' in msg_data and isinstance(msg_data['voltage_percent'], int):
            self.battery_count = msg_data['voltage_percent']
            # if self.battery_count == 255:
            #    show box warning

        if 'yewei2_percent' in msg_data and isinstance(msg_data['yewei2_percent'], int):
            self.water_count = msg_data['yewei2_percent']
            # if self.water_count == 255:
            #    show box warning

        if 'Position_X' in msg_data and 'Position_Y' in msg_data:
            left_speed = msg_data['Position_X']
            right_speed = msg_data['Position_Y']
            if isinstance(left_speed, float) and isinstance(right_speed, float):
                self.line_speed = abs(msg_data['Position_X'] + msg_data['Position_Y']) / 2
            else:
                self.line_speed = 0

    def set_button_enable(self, enable=True):
        self.m_bpButtonAt_mini.setEnabled(enable)
        self.m_bpButtonMt_mini.setEnabled(enable)

    def show_mt_at(self, tab_name):
        if tab_name in range(Page_num) and tab_name != Page_show_box:
            if tab_name is Page_mt_mode:
                self.m_bpButtonAt_mini.show()
                self.m_bpButtonMt_mini.hide()
            else:
                self.m_bpButtonAt_mini.hide()
                self.m_bpButtonMt_mini.show()

            self.m_title_label_list[Lable_title_mode_select].setText(list_page_string[tab_name][Page_index_title])

    def on_click_mini_at(self, event):
        """这里是点击切换到到自动驾驶"""
        if event:
            pass

        if not self.link_mcu or not self.link_ros:
            self.show_box(show_box_loss, '')
        else:
            if self.m_bpButtonAt_mini.IsEnabled():
                self.show_box(show_box_turn_at, '')

    def on_click_mini_mt(self, event):
        """这里是点击切换到到手动驾驶"""
        if event:
            pass
        if not self.link_mcu or not self.link_ros:
            self.show_box(show_box_loss, '')
        else:
            if self.m_bpButtonMt_mini.IsEnabled():
                self.show_box(show_box_turn_mt, '')

    def on_timer_show(self):
        """标题栏刷新定时器"""
        # check
        if time.time() - self.received_time < 1:
            self.link_mcu = True
            self.link_ros = True
        else:
            self.link_mcu = False
            self.link_ros = False

        self.one_second_cnt += 1
        if self.one_second_cnt >= 5 * 10:
            self.one_second_cnt = 0
            self.show_time()

    def show_time(self):
        """显示时间函数"""
        localtime = time.localtime(time.time())

        str_time = '{:02}'.format(localtime.tm_hour) + ':' + '{:02}'.format(localtime.tm_min)
        self.m_title_label_list[Label_title_time].setText(str_time)

        str_water = '{:3}'.format(self.water_count) + '%'
        self.m_tail_label_list[Label_tail_water_percent].setText(str_water)

        str_odom = '{:.2f}'.format(self.odom_count) + 'km'
        self.m_tail_label_list[Label_tail_odom_percent].setText(str_odom)

        str_battery = '{:3}'.format(self.battery_count) + '%'
        self.m_title_label_list[Label_title_battery].setText(str_battery)

    def start(self):
        self.timer_show.start(100)  # 设定时间间隔
        self.show_time()

    def stop(self):
        self.timer_show.stop()
