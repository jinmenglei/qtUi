from config.setting import *
import time
import random
import base.U_util as Util
from base.U_app_qt import Q_App
from base.U_log import get_logger
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import os


class ModeWorkingPanel(Q_App):
    """手动驾驶的panel"""
    start_timer_show_signal = pyqtSignal()
    stop_timer_show_signal = pyqtSignal()
    start_timer_process_signal = pyqtSignal()
    stop_timer_process_signal = pyqtSignal()

    def __init__(self, base_frame):
        self.module_name = 'mode_working'
        self.logger = get_logger(self.module_name)
        Q_App.__init__(self, self.module_name, base_frame)

        # frame init
        self.setGeometry(QRect(0, 40, 800, 340))

        self.res_path = Util.get_res_path(self.module_name)
        self.current_process = [0, 0, 0]
        self.check_process_target = [0, 0, 0]
        self.degree = [0, 0, 0]
        self.count = 0
        self.map_select_path = None
        self.map_select_name = None
        self.working_status = 0

        self.label_back = QtWidgets.QFrame(self)
        self.label_back.setGeometry(QRect(28, 26, 228, 228))
        self.label_back.setStyleSheet("background-color: #FFFFFF;")

        self.m_bitmap_map_working = QtWidgets.QLabel(self)
        self.m_bitmap_map_working.setGeometry(QRect(34, 31, 217, 217))
        self.m_bitmap_map_working.setStyleSheet('color: #FFFFFF')

        self.map_label_name = QtWidgets.QLabel(self)
        self.map_label_name.setGeometry(QRect(8, 276, 270, 26))
        font = QtGui.QFont()
        font.setFamily("MicrosoftYaHei-Bold")
        font.setPointSize(19)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.map_label_name.setFont(font)
        self.map_label_name.setText('test name')
        self.map_label_name.setStyleSheet("color: #000000;")
        self.map_label_name.setAlignment(QtCore.Qt.AlignCenter)

        tmp_list = list_working_label_info
        for index in range(4):
            str_name = tmp_list[index][list_working_name]
            label_point = tmp_list[index][list_working_point]
            working_label = QtWidgets.QLabel(self)
            working_label.setText(str_name)
            working_label.setGeometry(label_point)
            font = QtGui.QFont()
            font.setFamily("MicrosoftYaHei-Bold")
            font.setPointSize(19)
            font.setBold(True)
            font.setItalic(False)
            font.setWeight(70)
            working_label.setFont(font)
            working_label.setStyleSheet('color: #333333')
            working_label.setAlignment(QtCore.Qt.AlignCenter)

        self.list_working_label_point_show = []
        for index in range(Working_point_num):
            working_label = QtWidgets.QLabel(self)
            working_label.setText('')
            working_label.setGeometry(QRect(380 + 130 * index, 195, 90, 20))
            font = QtGui.QFont()
            font.setFamily("MicrosoftYaHei-Bold")
            font.setPointSize(19)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            working_label.setFont(font)
            working_label.setStyleSheet('color: #333333')

            self.list_working_label_point_show.append(working_label)
        self.working_set_point(0, 0, 0)

        tmp_list = list_working_process_info
        self.list_working_cover_panel = []
        self.list_working_cover_text = []
        for index in range(Working_gauge_num):
            gray_point = tmp_list[index][list_working_gray_point]
            text_point = tmp_list[index][list_working_text_point]

            gray = QtWidgets.QLabel(self)
            gray.setGeometry(gray_point)
            gray.setPixmap(QtGui.QPixmap(self.res_path + '工作中-灰.png'))
            gray.setText('')

            cover_panel = QtWidgets.QFrame(self)
            cover_panel.setGeometry(gray_point)
            cover_panel.setFixedSize(0, 38)

            blue = QtWidgets.QLabel('', cover_panel)
            blue.setGeometry(QRect(0, 0, 380, 38))
            blue.setPixmap(QtGui.QPixmap(self.res_path + '工作中-蓝.png'))

            text_panel = QtWidgets.QFrame(self)
            text_panel.setGeometry(text_point)
            text_panel.setStyleSheet('background: transparent;')

            cover_text = QtWidgets.QLabel(text_panel)
            cover_text.setStyleSheet('background: transparent;')
            cover_text.setGeometry(QRect(0, 0, text_point.width(), text_point.height()))
            cover_text.setAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setFamily("MicrosoftYaHei-Bold")
            font.setPointSize(19)
            font.setBold(True)
            font.setItalic(False)
            font.setWeight(60)
            cover_text.setFont(font)
            cover_text.setStyleSheet('color: #0E0E31')

            self.list_working_cover_panel.append(cover_panel)
            self.list_working_cover_text.append(cover_text)

        self.list_working_button_bitmap = []

        bitmap = "border-image: url(:/mode_working/mode_working/暂停.png);"
        self.list_working_button_bitmap.append(bitmap)
        bitmap = "border-image: url(:/mode_working/mode_working/继续.png);"
        self.list_working_button_bitmap.append(bitmap)

        self.m_button_pause_continue = QtWidgets.QPushButton(self)
        self.m_button_pause_continue.setGeometry(QRect(286, 236, 224, 84))
        self.m_button_pause_continue.setStyleSheet(self.list_working_button_bitmap[self.working_status])
        self.m_button_pause_continue.released.connect(lambda: self.on_click_pause_continue())
        self.m_button_pause_continue.pressed.connect(lambda: self.on_click_pause_continue_down())

        self.m_button_cancel = QtWidgets.QPushButton(self)
        self.m_button_cancel.setGeometry(QRect(524, 236, 224, 84))
        self.m_button_cancel.setStyleSheet("border-image: url(:/mode_working/mode_working/取消.png);")
        self.m_button_cancel.released.connect(lambda: self.on_click_cancel())
        self.m_button_cancel.pressed.connect(lambda: self.on_click_cancel_down())

        self.timer_show = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_show.timeout.connect(lambda: self.on_timer_show())
        self.start_timer_show_signal.connect(lambda: self.timer_show.start(100))
        self.stop_timer_show_signal.connect(lambda: self.timer_show.stop())

        self.timer_process = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_process.timeout.connect(lambda: self.on_timer_process())
        self.start_timer_process_signal.connect(lambda: self.timer_process.start(2))
        self.stop_timer_process_signal.connect(lambda: self.timer_process.stop())

        self.timer_delay = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_delay.timeout.connect(lambda: self.on_timer_process())

        self.__init_callback()

    def __init_callback(self):
        self.subscribe_msg(self.msg_id.mode_working_show_map, self.show_map_callback)

    def show_map_callback(self, data_dict):
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if 'map_path' in msg_data and 'map_name' in msg_data:
            map_path = msg_data['map_path']
            if os.path.isfile(map_path):
                self.map_select_path = map_path
                if 'map_name' in msg_data:
                    self.map_select_name = msg_data['map_name']
                    return
            else:
                self.logger.fatal(str(map_path) + 'select path is no existed')
                return

        self.logger.warning(str(data_dict) + ' data error !!!')

    def on_timer_delay(self, event):
        if event:
            pass
        self.timer_delay.stop()

    def do_ui_update(self):
        for index in range(Working_gauge_num):
            if abs(self.check_process_target[index] - self.current_process[index]) < self.degree[index]:
                self.current_process[index] = self.check_process_target[index]
                self.list_working_cover_panel[index].setFixedSize(int(self.check_process_target[index]), 34)
                if self.timer_process.isActive():
                    self.timer_process.stop()
            elif self.check_process_target[index] > self.current_process[index]:
                self.current_process[index] = self.current_process[index] + self.degree[index]
                self.list_working_cover_panel[index].setFixedSize(self.current_process[index], 34)

            elif self.check_process_target[index] < self.current_process[index]:
                self.current_process[index] = self.current_process[index] - self.degree[index]
                if self.current_process[index] < 0:
                    self.current_process[index] = 0
                self.list_working_cover_panel[index].setFixedSize(self.current_process[index], 34)

    def on_timer_process(self):
        """标题栏刷新定时器"""
        self.do_ui_update()

    def on_click_pause_continue_down(self):
        """暂停继续按钮"""
        if self.timer_delay.isActive():
            return

        if self.working_status == 0:
            self.m_button_pause_continue.setStyleSheet("border-image: url(:/mode_working/mode_working/暂停-按下.png);")
        else:
            self.m_button_pause_continue.setStyleSheet("border-image: url(:/mode_working/mode_working/继续-按下.png);")

    def on_click_pause_continue(self):
        """暂停继续按钮"""

        if self.timer_delay.isActive():
            return

        if self.working_status == 0:
            self.m_button_pause_continue.setStyleSheet(self.list_working_button_bitmap[1])
            self.working_status = 1
            self.timer_show.stop()
            self.timer_process.stop()
            self.m_button_cancel.setEnabled(True)
            self.set_button_enable(True)
        else:
            self.m_button_pause_continue.setStyleSheet(self.list_working_button_bitmap[0])
            self.working_status = 0
            self.timer_show.start(100)
            self.m_button_cancel.setEnabled(False)
            self.set_button_enable(False)

    def on_click_cancel_down(self):
        """取消按钮"""
        if self.timer_delay.isActive():
            return

        if self.m_button_cancel.isEnabled():
            self.m_button_cancel.setStyleSheet("border-image: url(:/mode_working/mode_working/取消-按下.png);")

    def on_click_cancel(self):
        """取消按钮"""

        if self.timer_delay.isActive():
            return

        if self.m_button_cancel.isEnabled():
            self.m_button_cancel.setStyleSheet("border-image: url(:/mode_working/mode_working/取消.png);")
            self.show_box(show_box_work_cancel, '')

    def working_set_gauge(self, index, value):
        """设置进度条和显示内容"""
        if value < 0:
            value = 0
        if value > list_working_max_value[index]:
            value = list_working_max_value[index]

        if 0 <= index < Working_gauge_num:
            str_show = list_working_format_string[index].format(value) + list_working_label_unit[index]
            set_value = value / list_working_max_value[index] * check_panel_size
            self.check_process_target[index] = set_value
            self.degree[index] = abs(self.check_process_target[index] - self.current_process[index])/100
            self.list_working_cover_text[index].setText(str_show)

    def working_set_point(self, x, y, z):
        """设置坐标的位置"""
        self.list_working_label_point_show[Working_point_x].setText('X:' + '{:4.1f}'.format(x))
        self.list_working_label_point_show[Working_point_y].setText('Y:' + '{:4.1f}'.format(y))
        self.list_working_label_point_show[Working_point_z].setText('Z:' + '{:4.1f}'.format(z))

    def start(self):
        # test
        self.map_select_name = '地图1'
        self.map_select_path = ":/mode_map_select/mode_map_select/map1.pgm"
        # test
        if self.map_select_name is not None and self.map_select_path is not None:
            map_bitmap = QtGui.QPixmap(self.map_select_path).scaled(217, 217)

            self.m_bitmap_map_working.setPixmap(map_bitmap)
            self.map_label_name.setText(self.map_select_name)

            self.working_set_gauge(Working_gauge_progress, 1)
            self.working_set_gauge(Working_gauge_speed, 1)
            self.working_set_gauge(Working_gauge_efficiency, 1)

            self.current_process = [0, 0, 0]
            self.check_process_target = [0, 0, 0]
            self.degree = [0, 0, 0]

            self.working_status = 0

            self.start_timer_show_signal.emit()
            self.m_button_cancel.setEnabled(False)
        else:
            self.show_box(show_box_no_map, '')
        self.set_button_enable(False)

    def set_button_enable(self, enable):
        data_dict = {'button_enable': enable}
        self.logger.info('send msg base_frame_set_button_enable :' + str(data_dict))
        self.send_msg_dispatcher(self.msg_id.base_frame_set_button_enable, data_dict)

    def stop(self):
        self.stop_timer_show_signal.emit()
        self.map_select_path = None
        self.map_select_name = None

    def show_ui_update(self):
        self.count = self.count + 1
        if self.count >= 10:
            self.count = 0

            progress_value = random.randint(0, 100)
            speed_value = random.random() * 0.7
            e_value = random.randint(0, 100)
            self.working_set_gauge(Working_gauge_progress, progress_value)
            self.working_set_gauge(Working_gauge_speed, speed_value)
            self.working_set_gauge(Working_gauge_efficiency, e_value)
            self.timer_process.start(2)

            x_value = random.randint(0, 100)
            y_value = random.randint(0, 100)
            z_value = random.randint(0, 100)
            self.working_set_point(x_value, y_value, z_value)

    def on_timer_show(self):
        """标题栏刷新定时器"""
        self.show_ui_update()
