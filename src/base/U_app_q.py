"""
这个是基本的app模块,包含2个通信部分
对外的pipe
对内的queue
"""
from threading import Thread
import time
from base.U_log import get_logger
import base.U_util as Util
from base.U_ins import Ins
from queue import Queue
from base.U_msg import UMsg
from multiprocessing import Pipe
from multiprocessing import connection


class App(object):
    """send msg to other model"""
    def __init__(self, module_name):
        self.__app_name = module_name
        self.__ins = Ins()
        self.msg_id = UMsg()
        self.__queue = None
        self.__pipe_dispatcher_rec = None
        self.__pipe_dispatcher_send = None
        self.__logger = get_logger('app_' + self.__app_name)
        self.__subscriber_dict = {}
        self.__logger.info('init model ' + self.__app_name)
        self.__is_shutdown = False
        self.__default_callback = None
        self.__multi_default_callback = None

        self.__init_thread_connect()
        self.__init_connection()
        # run self
        # self.__start__()

    def __init_thread_connect(self):
        self.__queue = Queue(0)

    def __init_connection(self):
        if 'dispatcher' in self.__app_name:
            self.__pipe_dispatcher_rec, self.__pipe_dispatcher_send = Pipe(False)
            self.__ins.add_module_queue(self.__app_name, self.__pipe_dispatcher_send)

            self.__ins.add_module_queue('dispatcher', self.__queue)

            if self.__app_name != self.msg_id.out_dispatcher:
                self.send_queue_module_manager()
        else:

            self.__ins.add_module_queue(self.__app_name, self.__queue)

    def add_dispatcher_pipe(self, dispatcher_name, pipe):
        """
        进程间使用pipe，线程间使用pysignal
        :param dispatcher_name:
        :param pipe:
        :return:
        """
        self.__ins.add_module_queue(dispatcher_name, pipe)

    def add_manager_dispatcher_pipe(self, pipe):
        """
        添加进程级通讯pipe对应关系,对外发
        :param pipe:
        :return:
        """
        self.__ins.add_module_queue('manager_dispatcher', pipe)

    def get_self_pipe(self):
        """
        获取pipe
        :return:
        """
        if self.__pipe_dispatcher_send is not None:
            return self.__pipe_dispatcher_send
        else:
            return self.__queue

    def subscribe_default(self, callback):
        """
        默认回调,给dispatcher 模块用
        :param callback:
        :return:
        """
        self.__default_callback = callback

    def subscribe_multi_default_callback(self, callback):
        """
        这个给进程间dispatcher用
        :param callback:
        :return:
        """
        self.__multi_default_callback = callback

    def subscribe_msg(self, msg_id, callback):
        """
        订阅回调,主要是内部queue的回调
        :param msg_id:
        :param callback:
        :return:
        """
        self.__subscriber_dict[msg_id] = callback
        msg_data = {'msg_id': msg_id, 'module_name': self.__app_name}
        if self.msg_id.inner_dispatcher is not None and self.msg_id.inner_register_id is not None:

            self.send_msg_dispatcher(self.msg_id.inner_register_id, msg_data)

    def __del__(self):
        """
        释放本模块
        :return:
        """
        self.stop_message()

    def __start__(self):
        """
        启动模块通讯监听
        :return:
        """
        self.process = Thread(target=self.__run__app)
        self.process.start()
        if self.__pipe_dispatcher_rec is not None:
            self.multi_process = Thread(target=self.__run__multi__)
            self.multi_process.start()

    def __run__multi__(self):
        """
        负责进程间的pipe监听
        :return:
        """
        self.__logger.info(self.__app_name + ' __run__multi__ subscribe')
        while not self.__is_shutdown:
            data_dict = self.__pipe_dispatcher_rec.recv()
            if self.__multi_default_callback is not None:
                self.__multi_default_callback(data_dict)

            time.sleep(0.0001)

    def __deal_data_dict(self,data_dict):
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None:
            callback = self.__subscriber_dict.get(msg_id)
            if callback is not None:
                callback(data_dict)
            else:
                if self.__default_callback is not None:
                    self.__default_callback(data_dict)

    def __run__app(self):
        """
        负责queue的监听
        :return:
        """
        self.__logger.info(self.__app_name + ' callback_msg subscribe')
        while not self.__is_shutdown:
            if not self.__queue.empty():
                data_dict = self.__queue.get_nowait()
                self.__deal_data_dict(data_dict)
            time.sleep(0.0001)
        #
        print(self.__app_name + ' quit by user')
        self.__logger.info(self.__app_name + ' quit by user')

    def stop_message(self):
        """
        进程状态切换
        :return:
        """
        self.__logger.info(self.__app_name + 'stop')
        self.__is_shutdown = True
        self.__ins.delete_module(self.__app_name)

    def make_session(self, msg_dst):
        return str(self.__app_name) + '-to-' + str(msg_dst) + '-' + Util.get_uuid()

    def send_msg(self, msg_id, msg_dst, msg_data=None):
        """send msg to other model"""
        send_msg = {'msg_id': msg_id, 'msg_data': msg_data, 'msg_src': self.__app_name, 'msg_dst': msg_dst,
                    'msg_session': self.make_session(msg_dst)}

        send_queue = self.__ins.get_queue_by_module_name(msg_dst)

        if send_queue is not None :
            if isinstance(send_queue, connection.Connection):
                # print('send_queue' + str(send_queue))
                send_queue.send(send_msg)
            else:
                self.send_msg_inner(send_queue, send_msg)

    def send_msg_inner(self, send_queue, data_dict):
        if isinstance(send_queue, Queue):
            send_queue.put_nowait(data_dict)

    def send_msg_id_manager_dispatcher(self, msg_id):
        msg_data = {'msg_id': msg_id, 'module_name': self.__app_name}
        self.send_msg(self.msg_id.manager_register_msg_id, self.msg_id.out_dispatcher, msg_data)

    def send_data_dict_manager_dispatcher(self, data_dict):
        send_queue = self.__ins.get_queue_by_module_name(self.msg_id.out_dispatcher)

        if send_queue is not None and isinstance(send_queue, connection.Connection):
            # print('send_queue' + str(send_queue) + 'data:' + str(data_dict))
            send_queue.send(data_dict)

    def send_queue_module_manager(self):
        msg_data = {'module_name': self.__app_name, 'pipe': self.__pipe_dispatcher_send}
        self.send_msg(self.msg_id.manager_register_pipe, self.msg_id.out_dispatcher, msg_data)

    def send_msg_dispatcher(self, msg_id, msg_data=None):
        self.send_msg(msg_id, self.msg_id.inner_dispatcher, msg_data)

    def send_msg_out(self, msg_data=None):
        self.send_msg(self.msg_id.interface_ros_send_msg_out, self.msg_id.inner_dispatcher, msg_data)

    def show_box(self, index, tip):
        msg_data = {'index': index, 'tip': tip}
        # print(msg_data)
        self.send_msg_dispatcher(self.msg_id.ui_manager_show_box, msg_data)

    def mode_dispatcher(self, page_mode):
        msg_data = {'page_mode': page_mode}
        self.send_msg_dispatcher(self.msg_id.ui_manager_change_page, msg_data)
