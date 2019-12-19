import time
import cv2 as cv
import datetime
import base.U_util as Util
import os
# import rospy
from threading import Thread
from base.U_app import App
from base.U_log import get_logger
from queue import Queue


class VideoRecord(App):
    """recorld video for clear"""

    def __init__(self):
        self.module_name = 'video_record'
        App.__init__(self, self.module_name)
        self.logger = get_logger(self.module_name)
        # Message.__init__(self,mode_name='VideoRecord')
        self.cap = None
        self.fourcc = None
        self.out_file = None
        self.start_time = 0
        self.frequency = 8.0
        self.abspath = None
        # video record
        self.record_time = 180  # s
        self.file_size = 1000  # M
        self.save_path = Util.get_res_path('video_save')
        self.snap_flag = False
        self.write_file_queue = Queue()
        self.rtmp_queue = Queue()
        self.local_queue = Queue()

    def snap_req_callback(self, data_dict):
        self.snap_flag = True

    def write_file_queue_callback(self):
        self.logger.info('come in write_file_queue_callback')
        while True:
            time.sleep(0.01)
            if not self.write_file_queue.empty():
                frame = self.write_file_queue.get_nowait()
                if self.out_file is None:
                    # print('change name ')
                    self.set_out_file_name()
                self.check_record_time()

                if self.snap_flag:
                    self.snap_flag = False
                    cv.imwrite(self.save_path + 'snap_0.jpg', frame)
                    msg_data = {}
                    msg_data['save_path'] = self.abspath + '/snap_0.jpg'
                    # self.dispatcher.ui_2_ros(msg_id='snap_res', msg_type='control', msg_data=msg_data)
                self.out_file.write(frame)
        pass

    def rtmp_queue_callback(self):
        self.logger.info('come in write_file_queue_callback')
        pass

    def local_queue_callback(self):
        self.logger.info('come in write_file_queue_callback')
        pass

    def start(self):
        Util.add_thread(target=self.__run__)
        Util.add_thread(target=self.write_file_queue_callback)
        Util.add_thread(target=self.rtmp_queue_callback)
        Util.add_thread(target=self.local_queue_callback)

    def __run__(self):
        self.init_cap()
        time.sleep(2)
        while True:
            self.logger.info('to get video !')
            while not os.path.exists('/dev/video0'):
                # print('video not exist')
                time.sleep(1)
            self.logger.info('get video success!')
            self.main_loop()
            self.logger.fatal('find except')
            time.sleep(1)

    def init_cap(self):
        self.fourcc = cv.VideoWriter_fourcc(*'XVID')
        # self.fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')

    def set_out_file_name(self):
        if self.out_file is not None:
            self.out_file.release()
            self.out_file = None

        str_time = str(datetime.datetime.now())
        str_time = str_time[:19]
        self.out_file = cv.VideoWriter(self.save_path + str_time + '.avi', self.fourcc, self.frequency, (640, 480))

        self.start_time = time.time()
        self.check_file_size()

    def check_record_time(self):
        if time.time() - self.start_time >= self.record_time:
            # print('time:', time.time(), ' starttime:', self.start_time)
            self.set_out_file_name()

    def check_file_size(self):
        while self.get_real_size() > self.file_size:
            self.keep_file_size()

    def keep_file_size(self):
        file_list = os.listdir(self.save_path)
        file_list = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(self.save_path, x)))
        # print('file: ', file_list)
        os.remove(self.save_path + file_list[0])

    def get_real_size(self):
        size = 0.0
        for root, dirs, files in os.walk(self.save_path):
            size += sum([os.path.getsize(os.path.join(root, file)) for file in files])
        size = round(size / 1024 / 1024, 2)
        # print('size: ', size)
        return size

    def main_loop(self):
        try:
            self.cap = cv.VideoCapture(0)
            self.abspath = os.path.abspath(self.save_path)
            while self.cap.isOpened():
                # time.sleep(0.001)
                time_start = time.time()
                ret, frame = self.cap.read()
                if ret:
                    # print(time.time() - time_start)
                    # flip frame
                    # cv.imshow('frame', frame)
                    frame = cv.flip(frame, -1)

                    # set time flag
                    str_time = str(datetime.datetime.now())
                    str_time = str_time[:21]
                    cv.putText(frame, str_time, (30, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, self.get_text_color(frame), 1)
                    # self.rtmp_queue.put_nowait(frame)
                    # self.local_queue.put_nowait(frame)
                    self.write_file_queue.put_nowait(frame)

                time_sleep = time.time() - time_start
                # print(time.time(), time_sleep)
                if time_sleep < 1 / self.frequency:
                    time.sleep(1 / self.frequency - time_sleep)

        except Exception as e:
            self.logger.info('Exception:' + str(e))
            self.out_file.release()
            self.cap.release()
            pass

    def get_text_color(self, frame):
        sum_bgr = 0

        for index in range(30, 230):
            b, g, r = frame[index, 25]
            sum_bgr = sum_bgr + b + g + r

        if sum_bgr > 125 * 200 * 3:
            return 0, 0, 0
        else:
            return 255, 255, 255


# test code
if __name__== '__main__':
    # from service.dispatcher import Dispatcher
    # dispatcher = Dispatcher()
    vr = VideoRecord()
    vr.start()
