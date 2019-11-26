from multiprocessing import Process
from usher.ui.ui_manager import UiManager
import time
from base.U_log import get_logger
from usher.service.service_manager import ServiceManger
from base.U_dispatcher import UDispatcher
from base.U_msg import UMsg
import sys
import os
import signal


class Manager:
    def __init__(self):
        self.logger = get_logger('Manager')
        self.manager_dispatcher = UDispatcher(UMsg.manager_dispatcher)
        self.manager_dispatcher.start()
        self.manager_pipe = self.manager_dispatcher.get_self_pipe()
        self.process_ui = None
        self.process_service = None

    def run_service_process(self, manager_pipe):
        self.logger.info('begin to start run_service_process')
        manager = ServiceManger(manager_pipe)
        manager.start()
        while True:
            time.sleep(1)

    def run_ui_process(self, manager_pipe):
        self.logger.info('begin to start run_ui_process')
        manager = UiManager(manager_pipe)
        manager.start()
        while True:
            time.sleep(1)

    def start(self):

        try:
            self.logger.info('get queue ' + str(self.manager_pipe))
            self.process_ui = Process(target=self.run_ui_process, args=(self.manager_pipe,), name='process_main')
            self.process_ui.start()
            self.logger.info('process_ui start ok')
            self.process_service = Process(target=self.run_service_process, name='process_child', args=(self.manager_pipe,))
            self.process_service.start()
            self.logger.info('process_service start_ok')
            while True:
                time.sleep(1)
        except KeyboardInterrupt as e:
            self.logger.fatal(' ########################## exit by : ' + str(e))
            self.logger.info('########################## kill process_ui.pid : ' + str(self.process_ui.pid))
            os.kill(self.process_ui.pid, signal.SIGKILL)
            self.logger.info('########################## kill process_service.pid : ' + str(self.process_service.pid))
            os.kill(self.process_service.pid, signal.SIGKILL)
            self.logger.info('########################## kill self.pid : ' + str(os.getpid()))
            time.sleep(1)
            os.kill(os.getpid(), signal.SIGKILL)
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
