#! /usr/bin/ python
import time
import logging
import rospy
import roslaunch
from threading import Thread
from rosgraph import masterapi,names
import os
import yaml

import psutil
import socket
import struct
import fcntl


# def getip(ethname):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])

def getipaddr():
    ditNet = psutil.net_if_addrs()

    if '192.168.' in str(ditNet):
            return True
    return False


class TaskThread(Thread):
    """roscore thread"""
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        roslaunch.rlutil._wait_for_master()
        # time.sleep(2)
        rosmaster = masterapi.Master(names.make_caller_id('rosparam-%s'%os.getpid()))
        while not rosmaster.hasParam('run_id'):
            time.sleep(1)
        while rosmaster.getParam('run_id') is '':
            time.sleep(1)

        logging.basicConfig(filename='/home/utry/xiaoyuan_logger.log', filemode="w",
                            format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S",
                            level=logging.INFO)
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        print('uuid' + uuid)

        # launch = roslaunch.parent.ROSLaunchParent(uuid, [
        #     "/home/huike/robot_ws/src/huanyu_robot_start/launch/Huanyu_robot_start.launch"])

        # launch2 = roslaunch.parent.ROSLaunchParent(uuid, [
        #     "/home/huike/robot_ws/src/huanyu_robot_start/launch/navigation_slam.launch"])

        launch_rosbrige = roslaunch.parent.ROSLaunchParent(uuid, [
            "/opt/ros/kinetic/share/rosbridge_server/launch/rosbridge_websocket.launch"])
        try:
            launch_rosbrige.start()
            # launch.start()
            # time.sleep(5)
            #
            # launch2.start()
            # rospy.loginfo("rospy.loginfo ##########")
            # logging.info("logging.info ##########")
            #
            # launch.spin()
            # launch2.spin()
            launch_rosbrige.spin()


        except Exception as e:
            print('I am except')
            rospy.logfatal(e)
            # logging.info("###### Exception occurred")

        finally:
            print('I am finally')
            # After Ctrl+C, stop all nodes from running
            #   launch.shutdown()
            #   launch2.shutdown()
            launch_rosbrige.shutdown()
        pass


if __name__ == '__main__':

    while not getipaddr():
        print ('hahahaha')
        time.sleep(2)
    time.sleep(2)
    task = TaskThread('utry_star_roscore')
    task.start()
    roslaunch.main(['roscore', '--core'])



