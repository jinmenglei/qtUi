from multiprocessing import Process
from usher.ui.ui_manager import UiManager
import time
from base.U_log import get_logger
from usher.service.service_manager import ServiceManger
from usher.ros_start.ros_manager import RosManager
from base.U_dispatcher import UDispatcher
from base.U_msg import UMsg
import sys
import os
import multiprocessing
import signal


class Manager:
    def __init__(self):
        self.logger = get_logger('Manager')
        self.logger.info('#######################################')
        self.logger.info('begin to start process')
        self.logger.info('#######################################')
        self.manager_lock = multiprocessing.Lock()
        self.manager_dispatcher = UDispatcher(UMsg.manager_dispatcher)
        self.manager_dispatcher.start()

        self.manager_pipe = {'pipe': self.manager_dispatcher.get_self_pipe(),
                             'lock': self.manager_dispatcher.get_self_lock()}
        self.process_ui = None
        self.process_service = None
        self.process_ros = None
        self.process_pool = {}

    def run_service_process(self, module_pipe):
        print('begin to start run_service_process')
        logger = get_logger('service_manager')
        logger.info('begin to start run_service_process')
        #
        try:
            manager = ServiceManger(module_pipe)
            manager.start()

            while True:
                time.sleep(1)
        except Exception as e:
            print('service find exception !!!!!!! : ' + str(e))
            logger.fatal('service find exception !!!!!!! : ' + str(e))
            time.sleep(2)

    def run_ui_process(self, module_pipe):
        print('begin to start run_ui_process')
        logger = get_logger('ui_manager')
        logger.info('begin to start run_ui_process')
        try:
            manager = UiManager(module_pipe)
            manager.start()
            while True:
                time.sleep(1)
        except Exception as e:
            print('ui find exception !!!!!!! : ' + str(e))
            logger.fatal('ui find exception !!!!!!! : ' + str(e))
            time.sleep(2)

    def run_ros_process(self, module_pipe):
        print('begin to start run_ros_process')
        logger = get_logger('ros_manager')
        logger.info('begin to start run_ros_process')

        try:
            manager = RosManager(module_pipe)
            manager.start()
            while True:
                time.sleep(1)
        except Exception as e:
            print('ros find exception !!!!!!! : ' + str(e))
            logger.fatal('ros find exception !!!!!!! : ' + str(e))
            time.sleep(2)

    def start(self):

        try:
            self.logger.info('get queue ' + str(self.manager_pipe))

            self.process_service = Process(target=self.run_service_process, args=(self.manager_pipe, ), name='process_child' )
            self.process_service.daemon = True
            time.sleep(1)
            self.process_service.start()
            self.logger.info('process_service start_ok')
            self.process_pool['process_service'] = self.process_service

            self.process_ui = Process(target=self.run_ui_process, args=(self.manager_pipe,), name='process_main')
            self.process_ui.daemon = True
            time.sleep(1)
            self.process_ui.start()
            self.logger.info('process_ui start ok')
            self.process_pool['process_ui'] = self.process_ui

            self.process_ros = Process(target=self.run_ros_process, args=(self.manager_pipe,), name='process_ros')
            # self.process_ros.daemon = True
            time.sleep(1)
            self.process_ros.start()
            self.logger.info('process_ros start ok')
            self.process_pool['process_ros'] = self.process_ros

            while True:
                # for key in self.process_pool:
                #     self.logger.info('check process :' + str(key) + 'pid: ' + str(self.process_pool[key].pid) +
                #                      'is_alive: ' + str(self.process_pool[key].is_alive()))
                # print('main process is still alive----refresh')
                time.sleep(1)
        except KeyboardInterrupt as e:
            self.logger.fatal(' ########################## exit by : ' + str(e))

            self.logger.info('########################## kill process_ui.pid : ' + str(self.process_ui.pid))
            self.process_ui.terminate()
            self.process_ui.join(3)
            # os.kill(self.process_ui.pid, signal.SIGKILL)
            self.logger.info('########################## kill process_ui.pid : ' + str(self.process_ros.pid))
            self.process_ros.terminate()
            self.process_ros.join(3)
            # os.kill(self.process_ros.pid, signal.SIGKILL)

            self.logger.info('########################## kill process_service.pid : ' + str(self.process_service.pid))
            self.process_service.terminate()
            self.process_service.join(3)
            # os.kill(self.process_service.pid, signal.SIGKILL)

            self.logger.info('########################## kill self.pid : ' + str(os.getpid()))
            time.sleep(1)
            # os.kill(os.getpid(), signal.SIGKILL)
            sys.exit(0)


# test_code
if __name__ == '__main__':

    #     logger = get_logger(__name__)
    # # try:
    #     logger.info('logging init success')
    #     logger.info('begin to start ui_main')
    #
    #     dispatcher = Dispatcher()
    #     dispatcher.start()
    #     logger.info('dispatcher start')
    #
    #     manger = UiManger(dispatcher)
    #     manger.start()
    #     logger.info('manager start')
    #
    #     update = UpdateTask(dispatcher)
    #     update.start()
    #     logger.info('update_task start')
    #
    #     video_record = VideoRecord(dispatcher)
    #     video_record.start()
    #     logger.info('VideoRecord start')

        while True:
            time.sleep(2)
    # except Exception as e:
    #     logger.fatal('end process by :' + str(e))
