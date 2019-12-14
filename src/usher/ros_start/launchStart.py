#! /usr/bin/ python
import time
import logging
import rospy
import roslaunch
from threading import Thread
from rosgraph import masterapi,names
import os
import yaml
from base.U_app import App
from base.U_log import get_logger
import base.U_util as Util
import config.setting as setting


class LaunchThread(App):
    """roscore thread"""
    def __init__(self):
        self.__module_name = 'LaunchThread'
        App.__init__(self, self.__module_name)
        self.__logger = get_logger(self.__module_name)
        self.launch_under_pan = None
        self.launch_sensor = None
        self.launch_amcl = None
        self.launch_running = None
        self.is_start = False
        self.is_stop = False
        self.is_shutdown = False
        self.uuid = None
        self.__init_callback()

    def __init_callback(self):
        self.subscribe_msg(self.msg_id.launch_start_control, self.control_callback)

    def control_callback(self, data_dict):
        self.__logger.info(str(data_dict))
        _, msg_data = Util.get_msg_id_data_dict(data_dict)
        if 'ros_start' in msg_data:
            if msg_data['ros_start']:
                if self.is_start:
                    self.__logger.warning(' is starting please wait')
                else:
                    self.__logger.info('start launch begin')
                    Util.add_thread(target=self.start_launch_thread)
            else:
                if self.is_stop:
                    self.__logger.warning(' is stopping please wait')
                else:
                    self.__logger.info('stop launch begin')
                    Util.add_thread(target=self.stop_launch_thread)

    def start_launch_thread(self):
        try:
            self.launch_sensor = roslaunch.parent.ROSLaunchParent(self.uuid, [
                "/home/utry/catkin_ws/src/xiaoyuan_robot_v2/launch/xiaoyuan_robot_start_sensor.launch"])

            self.launch_amcl = roslaunch.parent.ROSLaunchParent(self.uuid, [
                "/home/utry/catkin_ws/src/xiaoyuan_robot_v2/launch/xiaoyuan_robot_start_amcl.launch"])

            self.launch_running = roslaunch.parent.ROSLaunchParent(self.uuid, [
                "/home/utry/catkin_ws/src/linerunning_v2/launch/xiaoyuan_clear.launch"])

            self.is_shutdown = False
            self.is_start = True

            self.__logger.info('begin to  sensor!')
            self.launch_sensor.start()
            self.__logger.info('end to sensor!')

            time.sleep(5)

            self.__logger.info('begin to amcl!')
            self.launch_amcl.start()
            self.__logger.info('end to amcl!')

            time.sleep(5)

            self.__logger.info('begin to running !')
            self.launch_running.start()
            self.__logger.info('end to running!')
            self.is_start = False
            self.__logger.info('start end!!!!')

            while not self.is_shutdown:
                time.sleep(1)
            self.is_shutdown = False
            self.__logger.info('recived stop msg !!!')

            return
        except roslaunch.RLException as e:
            print('I am except')
            self.__logger.fatal(str(e))
            self.is_start = False

        finally:
            self.is_start = False
            print('I am finally')
            self.launch_sensor.shutdown()
            print(self.launch_sensor)
            self.launch_amcl.shutdown()
            print(self.launch_amcl)
            self.launch_running.shutdown()
            print(self.launch_running)
        pass

    def stop_launch_thread(self):
        try:
            self.is_stop = True
            self.is_shutdown = True
            while self.is_shutdown:
                time.sleep(1)
            self.launch_sensor.shutdown()
            time.sleep(1)
            self.launch_amcl.shutdown()
            time.sleep(1)
            self.launch_running.shutdown()
            self.is_stop = False
            self.__logger.info('stop end !!!!')
        except roslaunch.RLException as e:
            self.__logger.fatal(' ########## I am except')
            self.__logger.fatal(str(e))
            self.is_stop = False

        finally:
            self.is_stop = False
            self.__logger.fatal('I am finally')

    def start(self):
        self.__logger.info('##### start ' + self.__module_name)
        roslaunch.rlutil._wait_for_master()
        rosmaster = masterapi.Master(names.make_caller_id('rosparam-%s'%os.getpid()))
        while not rosmaster.hasParam('run_id'):
            time.sleep(1)
        while rosmaster.getParam('run_id') is '':
            time.sleep(1)

        time.sleep(1)

        self.send_msg_dispatcher(self.msg_id.mode_start_status, {'index': setting.start_ros, 'status': True})

        self.uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        print('uuid' + self.uuid)

        self.launch_under_pan = roslaunch.parent.ROSLaunchParent(self.uuid, [
            "/home/utry/catkin_ws/src/xiaoyuan_robot_v2/launch/xiaoyuan_robot_start_underpan.launch"])

        try:
            time.sleep(1)

            self.__logger.info('begin to start launch_under_pan!')
            self.launch_under_pan.start()
            self.__logger.info('launch_under_pan started!')

            time.sleep(5)

            self.send_msg_dispatcher(self.msg_id.mode_start_status, {'index': setting.start_launch, 'status': True})

            while True:
                # self.__logger.info('######### launch still alive')
                time.sleep(10)

        except roslaunch.RLException as e:
            print('I am except')
            self.__logger.fatal(str(e))

        finally:
            print('I am finally')
            if self.launch_sensor is not None:
                self.launch_sensor.shutdown()
            if self.launch_amcl is not None:
                self.launch_amcl.shutdown()
            if self.launch_running is not None:
                self.launch_running.shutdown()
        pass


if __name__ == '__main__':

    while not getipaddr():
        print ('hahahaha')
        time.sleep(2)
    time.sleep(2)
    task = TaskThread('utry_star_roscore')
    task.start()
    roslaunch.main(['roscore', '--core'])



