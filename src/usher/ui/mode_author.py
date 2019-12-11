from config.setting import *
import base.U_util as Util
import base.U_app_qt as AppQt
from base.U_log import get_logger
import time
import requests
import shutil
import base64
from PyQt5 import QtGui, QtCore


class ModeAuthorPanel(AppQt.Q_App):
    """手动驾驶的panel"""
    def __init__(self, base_frame):
        self.module_name = 'mode_author'
        self.logger = get_logger(self.module_name)
        AppQt.Q_App.__init__(self, self.module_name, base_frame)

        self.show_callback = self.start
        self.hide_callback = self.stop

        self.res_path = Util.get_res_path(self.module_name)
        self.input_cnt = 0
        self.one_second_cnt = 0
        self.password = '889972'
        self.input_password = ''
        self.error_show_cnt = 0
        self.mac_id = Util.get_mac_address()
        self.download_url = 'http://47.100.182.145:8080/qrcode/clearQrcode?macId=' + self.mac_id
        self.unlock_url = 'http://47.100.182.145:8080/lock/queryUnlockById?macId=' + self.mac_id
        self.logger.info('get qr_code url is : ' + str(self.download_url))
        self.logger.info('unlock url is : ' + str(self.unlock_url))
        self.download_file_name = self.res_path + 'Qr_d.png'
        self.qr_code_path = self.res_path + 'Qr.png'
        self.process_percent = 0

        self.m_bitmap_qr = AppQt.get_label_picture(self, AppQt.QRect(18, 120, 161, 161), self.qr_code_path)

        tmp_list = list_button_author_info
        self.list_key_button = []
        for index in range(12):
            rect = tmp_list[index][Author_button_point]
            style_sheet = 'QPushButton{border-image: url(:/mode_author/mode_author/' + \
                          str(tmp_list[index][Author_button_unselect]) + ')}' + \
                          'QPushButton:pressed{border-image: url(:/mode_author/mode_author/' + \
                          str(tmp_list[index][Author_button_select]) + ')}'

            button = AppQt.get_pushbutton(self, rect, style_sheet)

            button.setObjectName(str(tmp_list[index][Author_button_id]))

            button.clicked.connect(lambda: self.on_click_key(self.sender().objectName()))

            self.list_key_button.append(button)

        tmp_list = list_radio_author_string
        self.radio_list = []
        self.radio_bitmap_list = []

        bitmap = QtGui.QPixmap(':/mode_author/mode_author/' + tmp_list[Author_radio_off])
        self.radio_bitmap_list.append(bitmap)
        bitmap = QtGui.QPixmap(':/mode_author/mode_author/' + tmp_list[Author_radio_on])
        self.radio_bitmap_list.append(bitmap)

        # 设置属性,位置
        for index in range(6):
            rect = AppQt.QRect(307 + (26 + 37) * index, 57, 26, 26)
            path = ':/mode_author/mode_author/' + tmp_list[Author_radio_off]
            radio_button= AppQt.get_label_picture(self, rect, path)

            self.radio_list.append(radio_button)

        self.m_static_password_tip = AppQt.get_label_text(self, AppQt.QRect(191, 14, 418, 28), True, '请扫描二维码或 输入管理员密码', 28,
                                                    'MicrosoftYaHei-Bold','#333333')

        self.timer_show = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_show.timeout.connect(self.on_timer_show)

        self.timer_error_show = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_error_show.timeout.connect(self.on_timer_error_show)

        self.timer_delay = QtCore.QTimer(parent=self)  # 创建定时器
        self.timer_delay.timeout.connect(self.on_timer_delay)

        self.update_qr_code = False
        Util.add_thread(target=self.update_qr_code_function)
        self.lock_status = False
        self.unlock_status = False
        Util.add_thread(target=self.qr_code_lock_function)

    def qr_code_lock_function(self):
        while True:
            time.sleep(0.1)
            if self.isVisible():
                time.sleep(1)
                if self.get_unlock_status():
                    if self.isVisible():
                        self.unlock_status = True
                        self.input_cnt = 0
                        self.input_password = ''
                        self.mode_dispatcher(Page_check)
            else:
                if not self.lock_status:
                    self.lock_status = True

    def get_unlock_status(self):
        # test
        try:
            ublock_url = self.unlock_url
            request = requests.get(ublock_url)
            data_dict = request.json()
            self.logger.debug('get msg :' + str(request.json()))
            if 'code' in data_dict:
                code = data_dict['code']
                if code == 0:
                    self.logger.info('unlock from other way!')
                    return True
                else:
                    self.logger.debug('device is locked!')
                    return False
        except:
            self.logger.warning('find error')
            return  False

    def update_qr_code_function(self):
        try_time = 10
        while try_time > 0:
            try:
                try_time -= 1
                if self.get_packet():
                    return
                else:
                    time.sleep(60)
            except:
                self.logger.fatal('fail update qr_code')
                time.sleep(60)

    def get_packet(self):
        # get packet
        self.logger.info('begin to download ' + str(self.download_url))

        download_url = self.download_url
        request = requests.get(download_url)
        # print(request.text.lstrip())
        with open(self.download_file_name, 'wb') as f:
            img = base64.b64decode(request.text.replace(' data:image/png;base64,', ''))
            f.write(img)
            f.close()

        if not self.compare_qr_code():
            self.logger.info('update qr_code')
            shutil.copy2(self.download_file_name, self.qr_code_path)
            self.update_qr_code = True
            return True

    def compare_qr_code(self):
        ret, md5sum_download = Util.get_md5sum(self.download_file_name)
        if ret == 'ok':
            ret, md5sum_current = Util.get_md5sum(self.qr_code_path)
            if md5sum_current == md5sum_download:
                self.logger.info('two png is same!!')
                return True
        self.logger.info('two png not same!!' + str(md5sum_download) + ' : ' + str(md5sum_current))
        return False

    def get_qr_code_unlock(self):
        update_url = 'http://47.100.182.145:9200/update_info?'
        update_url = update_url + 'packageName=update' + '&versionName=1'

        while self.IsShown():
            request = requests.get(update_url)
            json_request = request.json()

            if json_request['diffUpdate']:
                self.json_request = json_request
                # self.show_box(show_box_update, '')
                return True

            time.sleep(60)
        return False

    def on_timer_delay(self):
        self.timer_delay.stop()

    def timer_show_ui(self):
        if self.update_qr_code:
            self.update_qr_code = False
            Qrbitmap = QtGui.QPixmap(self.qr_code_path).scaled(161, 161)
            self.m_bitmap_qr.setPixmap(Qrbitmap)

    def on_timer_show(self):
        """标题栏刷新定时器"""
        self.timer_show_ui()

    def radio_show(self):
        """单选框显示"""
        for index in range(6):
            if self.input_cnt > index:
                self.radio_list[index].setPixmap(self.radio_bitmap_list[Author_radio_on])
            else:
                self.radio_list[index].setPixmap(self.radio_bitmap_list[Author_radio_off])

    def timer_error_show_ui(self):
        self.error_show_cnt += 1
        x_point = 329
        if self.error_show_cnt >= 10:
            self.timer_error_show.stop()
            self.m_static_password_tip.setText('请扫描二维码或 输入管理员密码')
            self.error_show_cnt = 0
        else:
            if self.error_show_cnt % 2 == 0:
                x_point = 300
            else:
                x_point = 360

        for index in range(6):
            self.radio_list[index].move((37 + 26) * index + x_point, 57)

    def on_timer_error_show(self):
        """错误显示提示"""
        self.timer_error_show_ui()

    def on_click_key(self, str_index):
        """数字键盘点击事件处理"""
        # 删除操作
        index = int(str_index)
        if self.unlock_status:
            self.logger.warning('unlock by qr code input disable')
            return

        if self.timer_delay.isActive():
            return

        if self.timer_error_show.isActive():
            pass
        else:
            if index == Author_button_id_delete:
                if self.input_cnt > 0:
                    self.input_cnt -= 1
                    self.input_password = self.input_password[:self.input_cnt]
            # 清除操作
            elif index == Author_button_id_clear:
                self.input_cnt = 0
                self.input_password = ''
            # 其他输入 0-9
            else:
                self.input_cnt += 1
                self.input_password += str(index - Author_button_id_delta)
                # 输入6位后自动判断是否正确
                if self.input_cnt == 6:
                    if self.input_password == self.password:
                        self.mode_dispatcher(Page_check)
                    else:
                        # 错误对话跨国
                        self.m_static_password_tip.setText('密码错误，请重新输入')
                        self.timer_error_show.stop()
                        self.timer_error_show.start(100)

                    self.input_cnt = 0
                    self.input_password = ''

            self.radio_show()

    def start(self):
        self.timer_show.start(200)
        self.input_cnt = 0
        self.error_show_cnt = 0
        self.input_password = ''
        self.timer_error_show.stop()
        self.m_static_password_tip.setText('请扫描二维码或 输入管理员密码')
        self.unlock_status = False
        self.lock_status = False

    def stop(self):
        self.timer_show.stop()
        self.timer_error_show.stop()
