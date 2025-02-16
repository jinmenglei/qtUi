from config.setting import *
import base.U_util as Util
import base.U_app_qt as AppQt
from base.U_log import get_logger
from PyQt5 import QtGui, QtCore


class ModeCheckPanel(AppQt.Q_App):
    """手动驾驶的panel"""
    def __init__(self, base_frame):
        self.module_name = 'mode_check'
        self.logger = get_logger(self.module_name)
        AppQt.Q_App.__init__(self, self.module_name, base_frame)

        self.res_path = Util.get_res_path(self.module_name)

        self.check_index = 0
        self.check_last_status = Check_status_idle
        self.check_list_all = check_list_all
        self.check_process_target = 0
        self.current_process = 0
        self.degree = 0
        self.link_4G = True
        self.link_ros = True
        self.link_mcu = True
        self.battery_count = 88
        self.water_count = 88
        self.release_stop = True
        self.fault_status = True
        self.origin_status = True

        AppQt.get_label_picture(self, AppQt.QRect(344, 30, 130, 140), ':/mode_check/mode_check/扑拉飞呀导入版本.gif')

        AppQt.get_label_picture(self, AppQt.QRect(210, 174, 380, 41), ':/mode_check/mode_check/自检进度条-灰.png')

        self.cover_panel = AppQt.get_sub_frame(self, AppQt.QRect(213, 178, 0, 34))

        AppQt.get_label_picture(self.cover_panel, AppQt.QRect(0, 0, 380, 34), ':/mode_check/mode_check/自检进度条-蓝.png')

        rect = AppQt.QRect(215, 237, 150, 24)
        self.m_static_check_title = AppQt.get_label_text(self, rect, False, '', 24, 'MicrosoftYaHei', '#333333')
        self.m_static_check_title.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        rect = AppQt.QRect(430, 237, 150, 24)
        self.m_static_check_subtitle = AppQt.get_label_text(self, rect, False, '', 24, 'MicrosoftYaHei', '#333333')
        self.m_static_check_subtitle.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        rect = AppQt.QRect(430, 270, 150, 24)
        self.m_static_check_result = AppQt.get_label_text(self, rect, False, '', 24, 'MicrosoftYaHei', '#333333')
        self.m_static_check_result.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.__check_list_init__()

        self.timer_show = QtCore.QTimer()  # 创建定时器
        self.timer_show.timeout.connect(lambda: self.on_timer_show())

        self.timer_process = QtCore.QTimer() # 创建定时器
        self.timer_process.timeout.connect(lambda: self.on_timer_process())

    def __check_list_init__(self):
        """检测列表初始化"""
        self.check_list_all[Check_4g][Check_content_function] = self.check_4g
        self.check_list_all[Check_ros][Check_content_function] = self.check_ros
        self.check_list_all[Check_mcu][Check_content_function] = self.check_mcu
        self.check_list_all[Check_battery][Check_content_function] = self.check_battery
        self.check_list_all[Check_water][Check_content_function] = self.check_water
        self.check_list_all[Check_release_stop][Check_content_function] = self.check_release_stop
        self.check_list_all[Check_fault][Check_content_function] = self.check_fault
        self.check_list_all[Check_origin][Check_content_function] = self.check_origin

    def start(self):
        self.check_index = 0
        self.check_process_target = 0
        self.current_process = 0
        self.check_last_status = Check_status_idle

        self.timer_show.start(200)
        self.timer_process.start(4)

    def stop(self):
        self.timer_show.stop()
        self.timer_process.stop()

    def set_check_label_show(self, index, str_show):
        """显示提示内容"""
        self.m_static_check_title.setText(self.check_list_all[index][Check_title])
        self.m_static_check_subtitle.setText(self.check_list_all[index][Check_content_subtitle])
        self.m_static_check_result.setText(str_show)

    def do_check_function(self, index):
        """检测总入口"""
        check_status = self.check_list_all[index][Check_content_function]()
        str_show = self.check_list_all[index][Check_content_result_info][check_status + 0]
        return check_status, str_show

    def timer_process_ui(self):
        if abs(self.check_process_target - self.current_process) < self.degree:
            self.current_process = self.check_process_target
            self.cover_panel.setFixedSize(int(self.check_process_target), 38)
        elif self.check_process_target > self.current_process:
            self.current_process = self.current_process + self.degree
            self.cover_panel.setFixedSize(self.current_process, 38)

        elif self.check_process_target < self.current_process:

            self.current_process = self.current_process - self.degree
            self.cover_panel.setFixedSize(self.current_process, 38)

    def on_timer_process(self):
        """标题栏刷新定时器"""
        self.timer_process_ui()

    def timer_show_ui(self):
        index = self.check_index

        if index < len(self.check_list_all):
            if self.check_last_status == Check_status_idle:
                self.set_check_label_show(index, '检测中')
                self.check_last_status = Check_status_checking
            elif self.check_last_status == Check_status_checking:
                check_status, str_show = self.do_check_function(index)
                self.set_check_label_show(index, str_show)
                if not check_status:
                    self.check_last_status = Check_status_ng
                else:
                    self.check_last_status = Check_status_pass
            elif self.check_last_status == Check_status_ng:
                self.timer_show.Stop()
                self.check_index = 0
                self.check_last_status = Check_status_idle
            elif self.check_last_status == Check_status_pass:
                self.check_last_status = Check_status_idle
                self.check_index += 1
                if index < len(self.check_list_all) - 1:
                    show_count = (index + 1) * check_panel_size / len(self.check_list_all)
                else:
                    show_count = check_panel_size
                self.check_process_target = show_count
                self.degree = (self.check_process_target - self.current_process) / 100
        else:
            if self.current_process == 380:
                self.timer_show.stop()
                self.check_index = 0
                self.mode_dispatcher(Page_map_select)

    def on_timer_show(self):
        """标题栏刷新定时器"""
        self.timer_show_ui()

    def check_4g(self):
        """检测4G状态"""
        return self.link_4G

    def check_ros(self):
        return self.link_ros

    def check_mcu(self):
        return self.link_mcu

    def check_battery(self):
        if self.battery_count < 30:
            return False
        else:
            return True

    def check_water(self):
        if self.water_count < 30:
            return False
        else:
            return True

    def check_release_stop(self):
        return self.release_stop

    def check_fault(self):
        return self.fault_status

    def check_origin(self):
        return self.origin_status
