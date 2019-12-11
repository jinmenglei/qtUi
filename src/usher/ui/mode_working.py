from config.setting import *
import random
import base.U_util as Util
import base.U_app_qt as AppQt
from base.U_log import get_logger
from PyQt5 import QtGui, QtCore
import os


class ModeWorkingPanel(AppQt.Q_App):
    """手动驾驶的panel"""
    def __init__(self, base_frame):
        self.module_name = 'mode_working'
        self.logger = get_logger(self.module_name)
        AppQt.Q_App.__init__(self, self.module_name, base_frame)

        self.res_path = Util.get_res_path(self.module_name)
        self.current_process = [0, 0, 0]
        self.check_process_target = [0, 0, 0]
        self.degree = [0, 0, 0]
        self.count = 0
        self.map_select_path = None
        self.map_select_name = None
        self.working_status = working_status_on
        self.move_speed = 0
        self.position_x = 0
        self.position_y = 0
        self.position_z = 0
        self.progress_percent = 0

        self.label_back = AppQt.get_sub_frame(self, AppQt.QRect(28, 26, 228, 228), 'background-color: #FFFFFF;')

        self.m_bitmap_map_working = AppQt.get_label_picture(self.label_back, AppQt.QRect(5, 5, 218, 218))

        self.map_label_name = AppQt.get_label_text(self, AppQt.QRect(8, 276, 270, 26), False, '', 26)

        tmp_list = list_working_label_info
        for index in range(4):
            rect = tmp_list[index][list_working_point]
            name = tmp_list[index][list_working_name]
            AppQt.get_label_text(self, rect, True, name, 26, 'MicrosoftYaHei-Bold', '#333333')

        self.list_working_label_point_show = []
        for index in range(Working_point_num):
            rect = AppQt.QRect(380 + 130 * index, 192, 90, 24)
            working_label = AppQt.get_label_text(self, rect, False, '', 24, 'MicrosoftYaHei', '#333333')

            self.list_working_label_point_show.append(working_label)

        self.working_set_point()

        tmp_list = list_working_process_info
        self.list_working_cover_panel = []
        self.list_working_cover_text = []
        for index in range(Working_gauge_num):
            rect = tmp_list[index][list_working_gray_point]
            path = ':/mode_working/mode_working/工作中-灰.png'
            AppQt.get_label_picture(self, rect, path)

            cover_panel = AppQt.get_sub_frame(self, rect)

            path = ':/mode_working/mode_working/工作中-蓝.png'
            AppQt.get_label_picture(cover_panel, AppQt.QRect(0, 0, 380, 38), path)

            rect = tmp_list[index][list_working_text_point]
            text_panel = AppQt.get_sub_frame(self, rect, 'QFrame{background: transparent}')

            cover_text = AppQt.get_label_text(text_panel, AppQt.QRect(0, 0, rect.width(), rect.height()), True, '', 26,
                                              'MicrosoftYaHei-Bold', '#0E0E32')
            cover_text.setStyleSheet('QLabel{background: transparent}')

            self.list_working_cover_panel.append(cover_panel)
            self.list_working_cover_text.append(cover_text)

        self.list_working_button_bitmap = []

        bitmap = 'QPushButton{border-image: url(:/mode_working/mode_working/暂停.png)}' + \
                 'QPushButton:pressed{border-image: url(:/mode_working/mode_working/暂停-按下.png)}'
        self.list_working_button_bitmap.append(bitmap)

        bitmap = 'QPushButton{border-image: url(:/mode_working/mode_working/继续.png)}' + \
                 'QPushButton:pressed{border-image: url(:/mode_working/mode_working/继续-按下.png)}'

        self.list_working_button_bitmap.append(bitmap)

        rect = AppQt.QRect(286, 236, 214, 74)
        style_sheet = self.list_working_button_bitmap[self.working_status]
        self.m_button_pause_continue = AppQt.get_pushbutton(self, rect, style_sheet)

        self.m_button_pause_continue.clicked.connect(lambda: self.on_click_pause_continue())

        rect = AppQt.QRect(524, 236, 214, 74)
        self.cancel_style_sheet_enable = 'QPushButton{border-image: url(:/mode_working/mode_working/取消.png)}' + \
                                         'QPushButton:pressed{border-image: url(:/mode_working/mode_working/取消-按下.png)}'

        self.cancel_style_sheet_disable = 'QPushButton{border-image: url(:/mode_working/mode_working/取消灰.png)}'
        self.m_button_cancel = AppQt.get_pushbutton(self, rect, self.cancel_style_sheet_enable)

        self.m_button_cancel.clicked.connect(lambda: self.on_click_cancel())

        self.timer_show = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_show.timeout.connect(lambda: self.on_timer_show())

        self.timer_process = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_process.timeout.connect(lambda: self.on_timer_process())

        self.timer_delay = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_delay.timeout.connect(lambda: self.on_timer_process())

        self.timer_start_delay = QtCore.QTimer(parent=self)
        self.timer_start_delay.timeout.connect(lambda: self.on_timer_start_delay())

        self.__init_callback()

    def on_timer_start_delay(self):
        msg_data = {'ros_start': True}
        self.send_msg_dispatcher(self.msg_id.launch_start_control, msg_data)
        self.timer_start_delay.stop()

    def __init_callback(self):
        self.subscribe_msg(self.msg_id.mode_working_show_map, self.show_map_callback)
        self.subscribe_msg(self.msg_id.mode_working_speed_notify, self.speed_notify_callback)
        self.subscribe_msg(self.msg_id.mode_working_position_notify, self.position_notify_callback)
        self.subscribe_msg(self.msg_id.mode_mode_working_progress_notify, self.progress_notify_callback)

    def progress_notify_callback(self, data_dict):
        _, msg_data = Util.get_msg_id_data_dict(data_dict)
        self.logger.info('receive msg ' + str(data_dict))
        if 'progress_percent' in msg_data:
            progress_percent = msg_data['progress_percent']
            if isinstance(progress_percent, int):
                if progress_percent >= 100:
                    self.progress_percent = 100
                else:
                    self.progress_percent = progress_percent

    def position_notify_callback(self, data_dict):
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if 'x' in msg_data and 'y' in msg_data and 'z' in msg_data:
            self.position_x = int(msg_data['x'])
            self.position_y = int(msg_data['y'])
            self.position_z = int(msg_data['z'])
        else:
            self.logger.warning(str(data_dict) + ' data error !!!')

        pass

    def speed_notify_callback(self, data_dict):
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if 'speed' in msg_data:
            self.move_speed = msg_data['speed']
        else:
            self.logger.warning(str(data_dict) + ' data error !!!')

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

            elif self.check_process_target[index] <= self.current_process[index]:
                self.current_process[index] = self.current_process[index] - self.degree[index]
                if self.current_process[index] < 0:
                    self.current_process[index] = 0
                self.list_working_cover_panel[index].setFixedSize(self.current_process[index], 34)

    def on_timer_process(self):
        """标题栏刷新定时器"""
        self.do_ui_update()

    def on_click_pause_continue(self):
        """暂停继续按钮"""

        if self.timer_delay.isActive():
            return

        if self.working_status == working_status_on:
            self.working_status = working_status_off
            self.m_button_pause_continue.setStyleSheet(self.list_working_button_bitmap[self.working_status])
            self.timer_show.stop()
            self.timer_process.stop()
            self.m_button_cancel.setEnabled(True)
            self.m_button_cancel.setStyleSheet(self.cancel_style_sheet_enable)
            self.set_button_enable(True)
            self.send_set_pause_msg(True)

        else:
            self.working_status = working_status_on
            self.m_button_pause_continue.setStyleSheet(self.list_working_button_bitmap[self.working_status])
            self.timer_show.start(200)
            self.m_button_cancel.setEnabled(False)
            self.m_button_cancel.setStyleSheet(self.cancel_style_sheet_disable)
            self.set_button_enable(False)
            self.send_set_pause_msg(False)

    def send_set_pause_msg(self, is_pause:bool):
        msg_data = {'msg_id': 'set_pause', 'msg_type': 'control',
                    'msg_data': 'no'}
        if is_pause:
            msg_data['msg_data'] = 'yes'
        self.send_msg_out(msg_data)

    def on_click_cancel(self):
        """取消按钮"""

        if self.timer_delay.isActive():
            return

        if self.m_button_cancel.isEnabled():
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

    def working_set_point(self):
        """设置坐标的位置"""
        self.list_working_label_point_show[Working_point_x].setText('X:' + '{:4d}'.format(int(self.position_x)))
        self.list_working_label_point_show[Working_point_y].setText('Y:' + '{:4d}'.format(int(self.position_y)))
        self.list_working_label_point_show[Working_point_z].setText('Z:' + '{:4d}'.format(int(self.position_z)))

    def start(self):
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

            self.working_status = working_status_on
            self.send_set_pause_msg(False)

            self.timer_show.start(200)
            self.timer_start_delay.start(10000)
            self.count = 11
            self.show_ui_update()
            self.m_button_pause_continue.setStyleSheet(self.list_working_button_bitmap[self.working_status])
            self.m_button_cancel.setEnabled(False)
            self.m_button_cancel.setStyleSheet(self.cancel_style_sheet_disable)
        else:
            self.show_box(show_box_no_map, '')
        self.set_button_enable(False)

    def set_button_enable(self, enable):
        data_dict = {'button_enable': enable}
        self.logger.info('send msg base_frame_set_button_enable :' + str(data_dict))
        self.send_msg_dispatcher(self.msg_id.base_frame_set_button_enable, data_dict)

    def stop(self):
        msg_data = {'ros_start': False}
        self.send_msg_dispatcher(self.msg_id.launch_start_control, msg_data)
        self.timer_show.stop()
        self.timer_start_delay.stop()
        self.map_select_path = None
        self.map_select_name = None

    def show_ui_update(self):
        self.count = self.count + 1
        if self.count >= 10:
            self.count = 0

            progress_value = self.progress_percent
            speed_value = self.move_speed
            e_value = int(self.move_speed * 0.62 * 3600)

            self.working_set_gauge(Working_gauge_progress, progress_value)
            self.working_set_gauge(Working_gauge_speed, speed_value)
            self.working_set_gauge(Working_gauge_efficiency, e_value)
            self.timer_process.start(4)

            # x_value = random.randint(0, 100)
            # y_value = random.randint(0, 100)
            # z_value = random.randint(0, 100)
            self.working_set_point()

    def on_timer_show(self):
        """标题栏刷新定时器"""
        self.show_ui_update()
