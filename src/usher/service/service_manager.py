from base.U_app import App
from base.U_log import get_logger
from usher.service.interface_ros import InterfaceRos
from usher.service.video_record import VideoRecord
from usher.service.Update_task import UpdateTask
from base.U_dispatcher import UDispatcher
import time


class ServiceManger(App):
    def __init__(self, manager_pipe):
        self.module_name = 'service_manager'
        App.__init__(self, self.module_name)
        self.dispatcher = UDispatcher(self.msg_id.service_dispatcher, manager_pipe)
        self.__logger = get_logger(self.module_name)

    def start(self):
        self.__logger.info('start service_manger!')
        interface_ros = InterfaceRos()
        interface_ros.start()
        self.__logger.info('start interface_ros ok')
        video_record = VideoRecord()
        video_record.start()
        self.__logger.info('start video_record ok !')
        update_task = UpdateTask()
        update_task.start()
        self.__logger.info('start update_task Ok!')
        interface_ros.init_ros_node()
        self.__logger.info('start init_ros_node Ok!')
        while True:
            time.sleep(1)
