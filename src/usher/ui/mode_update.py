from config.setting import *
import os
import base.U_util as Util
import base.U_app_qt as AppQt
from base.U_log import get_logger
from PyQt5 import QtGui, QtCore


class ModeUpdate(AppQt.Q_App):
    """手动驾驶的panel"""
    def __init__(self, base_frame):
        self.module_name = 'Update'
        AppQt.Q_App.__init__(self, self.module_name, base_frame, AppQt.QRect(0, 40, 800, 340))
        self.logger = get_logger(self.module_name)

        self.res_path = Util.get_res_path(self.module_name)

        self.check_index = 0
        self.check_last_status = Check_status_idle
        self.Update_list_all = Update_list_all
        self.check_process_target = 0
        self.current_process = 0
        self.degree = 0
        self.update_index = 0
        self.show_update_flag = False
        self.update_status = False
        self.process_percent = 0

        # gif 动图
        AppQt.get_label_picture(self, QRect(335, 20, 130, 140), ':/update/Update/扑拉飞呀导入版本.gif')

        AppQt.get_label_picture(self, QRect(210, 174, 380, 41), ':/update/Update/自检进度条-灰.png')

        cover_panel = AppQt.get_sub_frame(self, QRect(213, 178, 0, 34))

        AppQt.get_label_picture(cover_panel, QRect(0, 0, 380, 34), ':/update/Update/自检进度条-蓝.png')

        self.m_static_check_title = AppQt.get_label_text(self, QRect(215, 237, 150, 24), False, 'test',
                                                         24, 'MicrosoftYaHei', '#333333')
        self.m_static_check_title.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.m_static_check_subtitle = AppQt.get_label_text(self, QRect(430, 237, 150, 24), False, 'test',
                                                            24, 'MicrosoftYaHei', '#333333')
        self.m_static_check_subtitle.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.m_static_check_result = AppQt.get_label_text(self, QRect(430, 270, 150, 24), False, 'test',
                                                          24, 'MicrosoftYaHei', '#333333')
        self.m_static_check_result.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.__check_list_init__()

        self.timer_show = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_show.timeout.connect(lambda: self.on_timer_show())

        self.timer_process = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_process.timeout.connect(lambda: self.on_timer_process())

        self.__init_callback()

    def __init_callback(self):
        self.subscribe_msg(self.msg_id.mode_update_process, self.update_process)
        self.subscribe_msg(self.msg_id.mode_update_change_result_status, self.change_result_status)

    def change_result_status(self, data_dict):
        if 'msg_data' in data_dict:
            msg_data = data_dict['msg_data']
            if 'update_node' in msg_data:
                update_node = msg_data['update_node']
                if update_node in range(Update_cnt):
                    if 'update_status' in msg_data:
                        update_status = msg_data['update_status']
                        self.Update_list_all[update_node][Update_result_status] = update_status
                        self.logger.info('correct msg :' + str(data_dict))
                        return
        self.logger.warning(' error msg :' + str(data_dict))

    def update_process(self,data_dict):
        if 'msg_data' in data_dict:
            msg_data = data_dict['msg_data']
            if 'update_node' in msg_data:
                update_node = msg_data['update_node']
                if 'process' in msg_data:
                    if update_node in range(Update_cnt):
                        process = msg_data['process']
                        if 0 <= process <= 100:
                            self.Update_list_all[update_node][Update_process] = process
                            self.logger.info('correct msg :' + str(data_dict))
                            return
        self.logger.warning(' error msg :' + str(data_dict))

    def __check_list_init__(self):
        """检测列表初始化"""
        self.Update_list_all[Update_download][Update_function] = self.do_update_download
        self.Update_list_all[Update_md5][Update_function] = self.do_update_md5
        self.Update_list_all[Update_unzip][Update_function] = self.do_update_unzip
        self.Update_list_all[Update_base][Update_function] = self.do_update_base
        self.Update_list_all[Update_move][Update_function] = self.do_update_move
        self.Update_list_all[Update_ui][Update_function] = self.do_update_ui
        # self.check_list_all[Check_fault][Check_content_function] = self.check_fault()
        # self.check_list_all[Check_origin][Check_content_function] = self.check_origin()

    def do_update_md5(self):
        self.m_static_check_result.setText('校验中')

    def do_update_unzip(self):
        self.m_static_check_result.setText('解压中')

    def do_update_base(self):
        pass

    def do_update_move(self):
        pass

    def do_update_ui(self):
        pass

    def do_update_download(self):
        str_show = str(self.Update_list_all[Update_download][Update_process])
        self.m_static_check_result.setText(str_show)

    def start(self):
        self.check_index = 0
        self.check_process_target = 0
        self.current_process = 0
        self.check_last_status = Check_status_idle
        self.timer_show.start(100)
        self.timer_process.start(2)

    def stop(self):
        self.timer_show.stop()
        self.timer_process.stop()

    def set_check_label_show(self, index, str_show):
        """显示提示内容"""
        self.m_static_check_title.setText(self.Update_list_all[index][Check_title])
        self.m_static_check_subtitle.setText(self.Update_list_all[index][Check_content_subtitle])
        self.m_static_check_result.setText(str_show)

    def timer_process_ui(self):
        if abs(self.check_process_target - self.current_process) < self.degree:
            self.current_process = self.check_process_target
            self.cover_panel.setFixedSize(int(self.check_process_target), 38)
        elif self.check_process_target > self.current_process:
            self.current_process = self.current_process + self.degree
            self.cover_panel.setFixdSize(self.current_process, 38)

        elif self.check_process_target < self.current_process:
            self.current_process = self.current_process - self.degree
            self.cover_panel.setFixdSize(self.current_process, 38)

    def on_timer_process(self):
        """标题栏刷新定时器"""
        self.timer_process_ui()

    def on_timer_show(self):
        """标题栏刷新定时器"""
        self.timer_show_ui()

    def timer_show_ui(self):
        if self.Update_list_all[self.check_index][Update_result_status] == Update_status_pass:
            self.m_static_check_result.setText('通过')
            if self.check_index < len(self.Update_list_all) - 1:
                show_count = (self.check_index + 1) * check_panel_size / len(self.Update_list_all)
            else:
                show_count = check_panel_size

                # do update end
                # os.system('reboot')

            self.check_process_target = show_count
            self.degree = (self.check_process_target - self.current_process)/100

            self.check_index += 1
            self.update_index = self.check_index
            self.process_percent = 0

        elif self.Update_list_all[self.check_index][Update_result_status] == Update_status_idle:
            self.Update_list_all[self.check_index][Update_result_status] = Update_status_checking
            self.set_check_label_show(self.check_index, '')
            data_dict = {'update_node': self.check_index}
            self.send_msg_dispatcher(self.msg_id.update_task_do_process, data_dict)

        elif self.Update_list_all[self.check_index][Update_result_status] == Update_status_checking:
            self.Update_list_all[self.check_index][Update_function]()

        elif self.Update_list_all[self.check_index][Update_result_status] == Update_status_ng:
            self.m_static_check_result.setText('失败')
            self.mode_dispatcher(Page_mt_mode)
            print('do update fail')
            # return
