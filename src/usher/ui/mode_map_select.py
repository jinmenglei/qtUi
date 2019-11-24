from config.setting import *
import time
import base.U_util as Util
from base.U_app_qt import Q_App
from base.U_log import get_logger
from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class ModeMapSelectPanel(Q_App):
    """手动驾驶的panel"""
    start_timer_show_signal = pyqtSignal()
    stop_timer_show_signal = pyqtSignal()

    def __init__(self, base_frame):
        self.module_name = 'mode_map_select'
        self.logger = get_logger(self.module_name)
        Q_App.__init__(self, self.module_name, base_frame)

        # frame init
        self.setGeometry(QRect(0, 40, 800, 340))

        self.res_path = Util.get_res_path(self.module_name)

        self.timer_show = QtCore.QTimer()  # 创建定时器
        self.timer_show.timeout.connect(lambda: self.on_timer_show())
        self.start_timer_show_signal.connect(lambda: self.timer_show.start(1000))
        self.stop_timer_show_signal.connect(lambda: self.timer_show.stop())

        self.list_map_button = []
        self.list_map_label = []
        for index in range(Map_select_num):
            button_id = list_button_map_string[index][Map_button_id]
            button_bitmap = "border-image: url(:/mode_map_select/mode_map_select/" + \
                            str(list_button_map_string[index][Map_button_path]) + ");"

            label = QtWidgets.QFrame(self)
            label.setGeometry(list_button_map_string[index][Map_back_point])
            label.setStyleSheet("background-color: #FFFFFF;")

            map_bpbutton = QtWidgets.QPushButton(self)
            map_bpbutton.setGeometry(list_button_map_string[index][Map_button_point])
            map_bpbutton.setStyleSheet(button_bitmap)
            map_bpbutton.setObjectName(str(button_id))

            map_bpbutton.clicked.connect(lambda: self.on_click_map_button(int(self.sender().objectName())))

            self.list_map_button.append(map_bpbutton)

            label_string = list_button_map_string[index][Map_label_string]
            label_point = list_button_map_string[index][Map_label_point]

            map_label = QtWidgets.QLabel(self)
            map_label.setGeometry(label_point)
            map_label.setText(label_string)

            font = QtGui.QFont()
            font.setFamily("MicrosoftYaHei-Bold")
            font.setPointSize(19)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)

            map_label.setFont(font)
            map_label.setStyleSheet('color: #000000')

            self.list_map_label.append(map_label)

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
        self.start_timer_show_signal.emit()

    def stop(self):
        self.stop_timer_show_signal.emit()

    def on_timer_show(self):
        """标题栏刷新定时器"""
        pass


