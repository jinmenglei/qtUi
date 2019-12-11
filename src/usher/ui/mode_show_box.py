from config.setting import *
import base.U_util as Util
import base.U_app_qt as AppQt
from base.U_log import get_logger
from PyQt5 import QtCore


class ModeShowBox(AppQt.Q_App):
    """手动驾驶的panel"""
    def __init__(self, base_frame):
        self.module_name = 'show_box'
        self.logger = get_logger(self.module_name)
        AppQt.Q_App.__init__(self, self.module_name, base_frame, QRect(0, 0, 800, 480),
                             'QFrame{border-image: url(:/show_box/show_box/半透明.png)}'
                             'QFrame{background: transparent}')

        self.res_path = Util.get_res_path(self.module_name)
        self.index = 0

        self.m_bitmap_white = AppQt.get_sub_frame(self, QRect(100, 53, 600, 374),
                                                  'QFrame{border-image: url(:/show_box/show_box/弹窗.png)}')

        style_sheet = 'QPushButton{border-image: url(:/show_box/show_box/否.png)}' + \
                      'QPushButton:pressed{border-image: url(:/show_box/show_box/否-点击.png)}'
        self.button_no = AppQt.get_pushbutton(self.m_bitmap_white, QRect(41, 223, 240, 70), style_sheet)

        self.button_no.clicked.connect(lambda: self.on_click_button_no())

        style_sheet = 'QPushButton{border-image: url(:/show_box/show_box/是.png)}' + \
                      'QPushButton:pressed{border-image: url(:/show_box/show_box/是-点击.png)}'
        self.button_yes = AppQt.get_pushbutton(self.m_bitmap_white, QRect(320, 223, 240, 70), style_sheet)

        self.button_yes.clicked.connect(lambda: self.on_click_button_yes())

        self.m_static_show = AppQt.get_label_text(self.m_bitmap_white, QRect(0, 70, 600, 94), True, '', 34,
                                                  'MicrosoftYaHei-Bold', '#333333')

        self.timer_show = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_show.timeout.connect(lambda: self.on_timer_show())

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

        self.hide()
        # self.send_destroy_show_box()

    def on_click_button_yes(self):
        """取消按钮"""
        if list_show_box_string[self.index][show_box_yes] is not None:
            self.mode_dispatcher(list_show_box_string[self.index][show_box_yes])
        elif self.index == show_box_start_error:
            self.logger.fatal('start error restart!')
            Util.do_restart()

        self.hide()
        # self.send_destroy_show_box()

    def start(self):
        self.timer_show.start(1000)

    def stop(self):
        self.timer_show.stop()

    def on_timer_show(self):
        """标题栏刷新定时器"""
        pass
