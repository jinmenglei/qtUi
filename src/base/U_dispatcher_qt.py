from base.U_log import get_logger
import base.U_util as Util
from base.U_app_qt import Q_App
from PyQt5.QtCore import  QRect


class UDispatcher(Q_App):
    """这个地方存放，状态，等信息，负责UI和外界的通讯"""

    def __init__(self, module_name, module_pipe=None):
        self.__module_name = module_name
        Q_App.__init__(self, self.__module_name, is_msg_center=True, geometry=QRect(0, 0, 0, 0))
        # self.hide()
        self.__logger = get_logger(self.__module_name)
        self.__init()
        # self.__msg_id_module_dict = {}
        if module_pipe is not None:
            self.add_manager_dispatcher_pipe(module_pipe)

    def __init(self):
        self.subscribe_msg(self.msg_id.inner_register_id, self.__subscribe_msg)
        self.subscribe_default(self.__msg_dispatcher)
        self.subscribe_multi_default_callback(self.__multi_msg_dispatcher)

    def __multi_msg_dispatcher(self, data_dict):
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)

        if msg_id is not None:
            module_name = self.msg_id_module_dict.get(msg_id)
            if isinstance(module_name, str):
                self.send_msg(msg_id, module_name, msg_data, msg_src=data_dict['msg_src'])

    def __msg_dispatcher(self,data_dict):
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)

        if msg_id is not None:
            module_name = self.msg_id_module_dict.get(msg_id)
            if isinstance(module_name, str):
                self.send_msg(msg_id, module_name, msg_data, msg_src=data_dict['msg_src'])
            else:
                if self.__module_name != self.msg_id.manager_dispatcher:
                    self.send_data_dict_manager_dispatcher(data_dict)

    def __subscribe_msg(self, data_dict):
        """
        subscribe msg_id with mode_name.

        :param data_dict: is a dict . include msg_id, mode_name

        Note: ##
        data_dict = {
            'msg_id' : 'register_msg_id',
            'msg_data' :
            {
                'msg_id' : 'xxxxx_id',
                'module_name' : 'xxxxxx'
            }
        }
        """
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None:
            msg_id = msg_data.get('msg_id')
            module_name = msg_data.get('module_name')
            if isinstance(msg_id, str) and isinstance(module_name, str):
                if msg_id == self.msg_id.inner_register_id:
                    self.__logger.info('register_msg_id ready for service !')
                else:
                    if msg_id in self.msg_id_module_dict:
                        self.__logger.warning('msg_id : ' + str(msg_id) + ' register again! old module_ is ' +
                                              str(self.msg_id_module_dict[msg_id]) + ' new module is ' +
                                              str(module_name))
                    else:
                        self.__logger.info('msg_id : ' + str(msg_id) + ' register to module :' + str(module_name))
                    self.msg_id_module_dict[msg_id] = module_name
                    self.send_msg_id_manager_dispatcher(msg_id)

    def start(self):
        """do nothing"""
        pass

# test code
if __name__ == '__main__':
    # dis = Dispatcher()
    pass
    # sendmsg = String()
    # # sendmsg_dict = {}
    # # sendmsg_dict['msg_id'] = 'snap_req'
    # # sendmsg_dict['msg_type'] = 'control'
    # #
    # sendmsg.data = str(json.dumps(json_str))

    # sendmsg.data = [1, 2, 3, 4, 5, 6, 7, 8]
    # test_pub.publish(sendmsg)
    # time.sleep(1)
    # print(pub.topicsMap)
    # data_dict = {'msg_id': 'test'}
    # pub.sendMessage('Dispatcher', data=data_dict)
    # print('end')