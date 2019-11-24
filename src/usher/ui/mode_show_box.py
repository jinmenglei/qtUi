from config.setting import *
import time
import base.U_util as Util
from base.U_app_qt import Q_App
from base.U_log import get_logger
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class ModeShowBox(Q_App):
    """手动驾驶的panel"""
    start_timer_show_signal = pyqtSignal()
    stop_timer_show_signal = pyqtSignal()
    show_tip_signal = pyqtSignal(int, str)
    def __init__(self, base_frame):
        self.module_name = 'show_box'
        self.logger = get_logger(self.module_name)
        Q_App.__init__(self, self.module_name,base_frame)

        self.setGeometry(QRect(0, 0, 800, 480))

        self.res_path = Util.get_res_path(self.module_name)
        self.index = 0

        self.setStyleSheet('border-image: url(:/show_box/show_box/半透明.png);\n')

        self.m_bitmap_white = QtWidgets.QFrame(self)
        self.m_bitmap_white.setStyleSheet('border-image: url(:/show_box/show_box/弹窗.png);'
                                          '\n background-image: url(:/show_box/show_box/弹窗.png);')
        self.m_bitmap_white.setGeometry(QRect(100, 53, 600, 374))

        self.bpbutton_no = QtWidgets.QPushButton(self)
        self.bpbutton_no.setGeometry(QRect(141, 276, 240, 70))
        self.bpbutton_no.setStyleSheet('border-image: url(:/show_box/show_box/否.png);')

        self.bpbutton_no.clicked.connect(lambda: self.on_click_button_no())
        self.bpbutton_no.pressed.connect(lambda: self.bpbutton_no.setStyleSheet(
            'border-image: url(:/show_box/show_box/否-点击.png);'))
        self.bpbutton_no.released.connect(lambda: self.bpbutton_no.setStyleSheet(
            'border-image: url(:/show_box/show_box/否.png);'))

        self.bpbutton_yes = QtWidgets.QPushButton(self)
        self.bpbutton_yes.setGeometry(QRect(420, 276, 240, 70))
        self.bpbutton_yes.setStyleSheet('border-image: url(:/show_box/show_box/是.png);')

        self.bpbutton_yes.clicked.connect(lambda: self.on_click_button_yes())
        self.bpbutton_yes.pressed.connect(lambda: self.bpbutton_yes.setStyleSheet(
            'border-image: url(:/show_box/show_box/是-点击.png);'))
        self.bpbutton_yes.released.connect(lambda: self.bpbutton_yes.setStyleSheet(
            'border-image: url(:/show_box/show_box/是.png);'))

        self.m_static_show = QtWidgets.QLabel(self.m_bitmap_white)
        self.m_static_show.setGeometry(QRect(127, 76, 346, 83))
        self.m_static_show.setAlignment(QtCore.Qt.AlignCenter)
        self.m_static_show.setStyleSheet('color: #333333 ;\n font: 60 Bold 34px \"MicrosoftYaHei\"; \n ')

        self.timer_show = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_show.timeout.connect(lambda: self.on_timer_show())
        self.start_timer_show_signal.connect(lambda: self.timer_show.start(1000))
        self.stop_timer_show_signal.connect(lambda: self.timer_show.stop())

        self.__init_callback()

    def __init_callback(self):
        self.subscribe_msg(self.msg_id.mode_show_box_show_tip, self.show_box_show_tip)

    def show_box_show_tip(self, data_dict):
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None:
            index, tip = Util.get_index_tip_msg_data(msg_data)
            if index is not None:
                pass
        pass

    def show_box_tip(self, index, tip=''):
        self.index = index
        self.m_static_show.setText(list_show_box_string[self.index][show_box_tip] + tip)

    def __show_box(self):
        if self.show_box_index is not None:
            self.index = self.show_box_index
            self.m_static_show.setText(list_show_box_string[self.index][show_box_tip] + self.show_box_tip)
        else:
            self.logger.warning('self.show_box_index is None')

    def send_destroy_show_box(self):
        self.send_msg_dispatcher(self.msg_id.ui_manager_destroy_show_box)

    def on_click_button_no(self):
        """取消按钮"""
        if list_show_box_string[self.index][show_box_no] is not None:
            self.mode_dispatcher(list_show_box_string[self.index][show_box_no])

        self.send_destroy_show_box()

    def on_click_button_yes(self):
        """取消按钮"""
        if list_show_box_string[self.index][show_box_yes] is not None:
            self.mode_dispatcher(list_show_box_string[self.index][show_box_yes])

        self.send_destroy_show_box()

    def start(self):
        self.start_timer_show_signal.emit()

    def stop(self):
        self.stop_timer_show_signal.emit()

    def on_timer_show(self):
        """标题栏刷新定时器"""
        pass
