from config.setting import *
import os
import base.U_util as Util
import base.U_app_qt as AppQt
from base.U_log import get_logger
from PyQt5 import QtGui, QtCore


class ModeStart(AppQt.Q_App):
    """手动驾驶的panel"""
    def __init__(self, base_frame):
        self.module_name = 'mode_start'
        # style_sheet = 'QFrame{border-image: url(:/mode_start/mode_start/start.png)}' \
        #               'QFrame{background: transparent}'
        AppQt.Q_App.__init__(self, self.module_name, base_frame, QRect(0, 0, 800, 480))
        self.logger = get_logger(self.module_name)

        self.res_path = Util.get_res_path(self.module_name)

        self.show_str = '正在启动请稍后'

        self.status_cnt = 0
        self.start_index = 0
        self.timeout_cnt = 0
        self.list_start_status = list_start_info

        self.picture_label = AppQt.get_label_picture(self, QRect(0, 0, 800, 480),
                                                     ':/mode_start/mode_start/start.png')

        rect = AppQt.QRect(0, 340, 800, 24)

        self.m_static_start_result = AppQt.get_label_text(self, rect, False, '', 24, 'MicrosoftYaHei', '#333333')
        self.m_static_start_result.setStyleSheet('background: transparent;')

        self.timer_show = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_show.timeout.connect(lambda: self.on_timer_show())

        self.__init_callback()

    def __init_callback(self):
        self.subscribe_msg(self.msg_id.mode_start_status, self.mode_status_update)
        pass

    def mode_status_update(self, data_dict):
        self.logger.info(str(data_dict))
        _, msg_data = Util.get_msg_id_data_dict(data_dict)
        if 'status' in msg_data and 'index' in msg_data:
            status = msg_data['status']
            index = msg_data['index']
            if isinstance(status, bool) and index in range(start_status_cnt):
                self.list_start_status[index][start_status] = status

    def start(self):
        self.timer_show.start(1000)

    def stop(self):
        self.timer_show.stop()

    def on_timer_show(self):
        """标题栏刷新定时器"""

        self.timer_show_ui()

    def timer_show_ui(self):
        str_show = ''

        if self.start_index >= start_status_cnt:
            self.mode_dispatcher(Page_mt_mode)
            return
        else:
            tmp_list = self.list_start_status[self.start_index]
        if not tmp_list[start_show_status]:
            str_show = tmp_list[start_show_begin]
            tmp_list[start_show_status] = True
            self.timeout_cnt = 0
            self.status_cnt = 0

        elif not tmp_list[start_status]:
            self.timeout_cnt += 1
            str_show = tmp_list[start_show_begin]
            if self.timeout_cnt >= 60:
                self.timeout_cnt = 0
                self.show_box(show_box_start_error, '')
                str_show = tmp_list[start_show_fail]
        elif tmp_list[start_status]:
            str_show = tmp_list[start_show_success]
            self.start_index += 1
            self.status_cnt = 0

        # self.logger.info(str_show)

        for index in range(self.status_cnt):
            str_show = str_show + '·'

        self.m_static_start_result.setText(str_show)
        self.status_cnt += 1
        if self.status_cnt >= 4:
            self.status_cnt = 0
