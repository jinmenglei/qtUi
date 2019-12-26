# update_task
import time
import requests
# import urllib3
import os
from config.setting import *
import zipfile
import shutil
import base.U_util as Util
from threading import Thread
from base.U_log import get_logger
from base.U_app import App
from third_party.config import get_value_by_key


class UpdateTask(App):
    def __init__(self):
        self.module_name = 'update_task'
        App.__init__(self, self.module_name)
        self.json_request = ''
        self.logger = get_logger(self.module_name)
        self.res_path = Util.get_res_path('Update')

        self.download_url = get_value_by_key('update_download_url', 'HOST_URL')
        self.logger.info('get download_url:' + str(self.download_url))
        if self.download_url is None:
            self.download_url = 'http://47.100.182.145:9200'

        self.update_url = get_value_by_key('update_url', 'HOST_URL')
        self.logger.info('get update_url:' + str(self.update_url))
        if self.update_url is None:
            self.update_url = 'http://47.100.182.145:9200/update_info?'

        self.update_function_list = []
        self.update_function_list_init()
        self.is_shutdown = False
        self.update_index = 0
        self.show_update_flag = False
        self.update_status = False
        self.process_percent = 0
        self.download_file_name = 'update.zip'
        self.__init_callback()

    def __init_callback(self):
        self.subscribe_msg(self.msg_id.update_task_do_process, self.update_task_do_process)

    def update_task_do_process(self,data_dict):
        if 'msg_data' in data_dict:
            msg_data = data_dict['msg_data']
            if 'update_node' in msg_data:
                update_node = msg_data['update_node']
                if update_node in range(len(self.update_function_list)):
                    callback = self.update_function_list[update_node]
                    if callback is not None:
                        self.logger.info('get info :' + str(data_dict))
                        callback(data_dict)
                        return
        self.logger.warning('error msg :' + str(data_dict))

    def check_out_version(self):
        update_url = self.update_url + 'packageName=update' + '&versionName=1'
        # print(update_url)
        update_time = 10
        time.sleep(5)
        while update_time > 0:
            update_time -= 1
            request = requests.get(update_url)
            json_request = request.json()

            if json_request['diffUpdate']:
                self.json_request = json_request
                # self.show_box(show_box_update, '')
                return True

            time.sleep(60)
        return False

    def __run__(self):
        try:
            self.check_out_version()
            self.logger.info('do update_task end!!')
        except:
            self.logger.fatal('find Exception')

    def start(self):
        Util.add_thread(target=self.__run__)

    def update_function_list_init(self):
        self.update_function_list.append(self.do_download_packet)
        self.update_function_list.append(self.do_update_md5)
        self.update_function_list.append(self.do_unzip)
        pass

    def do_download_packet(self, data_dict):
        # print(self.module_name)
        Util.add_thread(target=self.get_packet)

    def do_update_md5(self, data_dict):
        Util.add_thread(target=self.check_md5)

    def do_unzip(self, data_dict):
        Util.add_thread(target=self.unzip_file)

    def get_packet(self):
        # get packet
        self.logger.info(str(self.json_request))
        download_url = self.download_url + self.json_request['url'] + '?packageName=update'
        # print(download_url)

        request = requests.get(download_url, stream=True, verify=False)
        total_size = int(request.headers['Content-Length'])
        self.logger.info('total_size:' + str(total_size))
        temp_size = 0

        with open(self.res_path + self.download_file_name, "wb") as f:
            # iter_content()函数就是得到文件的内容，
            # 有些人下载文件很大怎么办，内存都装不下怎么办？
            # 那就要指定chunk_size=1024，大小自己设置，
            # 意思是下载一点写一点到磁盘。
            for chunk in request.iter_content(chunk_size=1024 * 100):
                if chunk:
                    temp_size += len(chunk)
                    f.write(chunk)
                    f.flush()
                    self.process_percent = int(temp_size/total_size * 100)
                    self.logger.info('get filesize :' + str(self.process_percent))
                    self.send_process(Update_download, self.process_percent)

        if temp_size == total_size:
            self.process_percent = 100
            result_status = Update_status_pass
            self.logger.info('download file: ' + str(self.download_file_name) + ' success!!')
        else:
            result_status = Update_status_ng
            self.logger.info('download file: ' + str(self.download_file_name) + ' fail !!! get filesize = '
                             + str(temp_size))
        self.send_process(Update_download, self.process_percent)
        time.sleep(1)
        self.send_result_status(Update_download, result_status)

    def send_process(self, update_node, process):
        data_dict = {'update_node': update_node, 'process': process}
        self.send_msg_dispatcher(self.msg_id.mode_update_process, data_dict)

    def unzip_file(self):
        filename = self.res_path + self.download_file_name
        if os.path.isdir(self.res_path + '/update'):
            shutil.rmtree(self.res_path + '/update')
        update_process = Update_status_pass
        if os.path.isfile(filename):
            zipfile_fp = zipfile.ZipFile(filename)
            zipfile_fp.extractall(self.res_path)
            self.logger.info('unzip ' + str(filename) + 'success!!')
            update_process = Update_status_pass
        else:
            update_process = Update_status_ng
            self.logger.info('unzip ' + str(filename) + 'fail , no such file or dict!!')

        self.send_result_status(Update_unzip, update_process)

    def send_result_status(self, update_node, update_status):
        data_dict = {'update_node': update_node, 'update_status': update_status}
        self.send_msg_dispatcher(self.msg_id.mode_update_change_result_status, data_dict)

    def check_md5(self):
        filename = self.res_path + self.download_file_name
        md5sum = self.json_request['md5']
        ret, md5sum_get = Util.get_md5sum(filename)

        if ret == 'ok':
            if md5sum == md5sum_get:
                self.logger.info('check sum pass!!')
                result_status = Update_status_pass
            else:
                self.logger.info('md5 checksum fail , target is ' + str(md5sum) + ' the calc is ' + str(md5sum_get))
                result_status = Update_status_ng
        else:
            self.logger.warning(str(ret))
            result_status = Update_status_ng

        self.send_result_status(Update_md5, result_status)
