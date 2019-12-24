from base.U_app import App
from base.U_log import get_logger
import base.U_util as Util
from third_party.database import DataBase


class CfgServer(App):
    def __init__(self):
        self.module_name = 'cfg_server'
        App.__init__(self, self.module_name)
        self.logger = get_logger(self.module_name)
        self.database = DataBase()
        self.database.create_table()
        self.__init_callback()

    def __init_callback(self):
        self.subscribe_msg(self.msg_id.cfg_server_set_odom, self.set_odom_callback)
        self.subscribe_msg(self.msg_id.cfg_server_get_odom, self.get_odom_callback)
        pass

    def get_odom_callback(self,datadict):
        self.get_odom()

    def get_odom(self):
        res = self.database.get_value_by_key('odom')
        self.logger.info('get odom :' + str(res))
        odom = '0.0'
        if res is not None:
            odom = res
        else:
            self.database.insert_key_value('odom', str(odom))
        msg_data = {'odom': odom}
        self.send_msg_dispatcher(self.msg_id.base_frame_odom_notify, msg_data)

    def set_odom_callback(self, data_dict):
        """
        {
            'msg_id' : 'cfg_server_set_odom',
            'msg_data': {
                'odom': 1.23
            }
        }
        :param data_dict:
        :return:
        """
        msg_id, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_id is not None and isinstance(msg_data, dict):
            self.logger.info('set_odom :' + str(data_dict))
            odom = msg_data['odom']
            self.database.update_key_value('odom', str(odom))

    def start(self):
        pass