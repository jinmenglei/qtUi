from multiprocessing import Process
from usher.ui.ui_manager import UiManager
import time
from base.U_log import get_logger
from usher.service.service_manager import ServiceManger
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
        self.manager_dispatcher = UDispatcher(UMsg.service_dispatcher)
        self.manager_dispatcher.start()

        self.process_pool = {}

    def start(self):

        try:
            self.logger.info('start manager')
            manager = ServiceManger()
            manager.start()

            manager = UiManager()
            manager.start()

        except KeyboardInterrupt as e:
            self.logger.fatal(' ########################## exit by : ' + str(e))

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
