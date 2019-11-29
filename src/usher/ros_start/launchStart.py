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


class LaunchThread(App):
    """roscore thread"""
    def __init__(self):
        self.__module_name = 'LaunchThread'
        App.__init__(self, self.__module_name)
        self.__logger = get_logger(self.__module_name)
        self.launch_ros_bridge = None
        self.__init_callback()

    def __init_callback(self):
        self.subscribe_msg(self.msg_id.launch_start_control, self.control_callback)

    def control_callback(self, data_dict):
        self.__logger.info(str(data_dict))
        if self.launch_ros_bridge is not None:
            self.launch_ros_bridge.shutdown()

    def run(self):
        roslaunch.rlutil._wait_for_master()
        rosmaster = masterapi.Master(names.make_caller_id('rosparam-%s'%os.getpid()))
        while not rosmaster.hasParam('run_id'):
            time.sleep(1)
        while rosmaster.getParam('run_id') is '':
            time.sleep(1)

        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        print('uuid' + uuid)

        # launch = roslaunch.parent.ROSLaunchParent(uuid, [
        #     "/home/huike/robot_ws/src/huanyu_robot_start/launch/Huanyu_robot_start.launch"])

        # launch2 = roslaunch.parent.ROSLaunchParent(uuid, [
        #     "/home/huike/robot_ws/src/huanyu_robot_start/launch/navigation_slam.launch"])

        self.launch_ros_bridge = roslaunch.parent.ROSLaunchParent(uuid, [
            "/opt/ros/kinetic/share/rosbridge_server/launch/rosbridge_websocket.launch"])
        try:
            self.launch_ros_bridge.start()
            # launch.start()
            # time.sleep(5)
            #
            # launch2.start()
            # rospy.loginfo("rospy.loginfo ##########")
            # logging.info("logging.info ##########")
            #
            # launch.spin()
            # launch2.spin()
            while True:
                # self.__logger.info('######### launch still alive')
                time.sleep(10)

        except roslaunch.RLException as e:
            print('I am except')
            self.__logger.fatal(str(e))

        finally:
            print('I am finally')
            self.launch_ros_bridge.shutdown()
        pass


if __name__ == '__main__':

    while not getipaddr():
        print ('hahahaha')
        time.sleep(2)
    time.sleep(2)
    task = TaskThread('utry_star_roscore')
    task.start()
    roslaunch.main(['roscore', '--core'])



