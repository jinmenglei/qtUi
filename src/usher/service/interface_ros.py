"""
ros 链接基础模块封装，本ros只有两个topic
"/ui_ros_topic" 这个ui模块向ros 发送消息的topic，消息以json形式发过去，在xiaoyuan_robot 里解析
“/ros_ui_topic” 这个时候ros 向ui发送消息的topic， 消息以json形式发送， 解析之后发送到interface_ros 模块
    interface_ros模块 处理之后分发到其他模块 interface 可能会很大
"""
import rospy
from base.U_app import App
from base.U_log import get_logger
import base.U_util as Util
import config.setting as setting
import time
from threading import Thread
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped
from rosgraph import Master
import roslaunch
from queue import Queue


class InterfaceRos(App):
    """to ros"""
    def __init__(self):
        self.module_name = 'interface_ros'
        App.__init__(self, self.module_name)
        self.link_ros = False
        self.link_mcu = False
        self.received_time = 0
        self.logger = get_logger(self.module_name)
        self.pub = None
        self.ros_is_running = False
        self.send_link_status = False
        self.master = None
        self.ui_ros_topic_is_sub = False
        self.callback_dict = {}
        self.__init_callback()
        self.msg_out_queue = Queue(0)
        Util.add_thread(target=self.msg_out_queue_callback)

    def msg_out_queue_callback(self):
        while True:
            if not self.msg_out_queue.empty():
                msg_data = self.msg_out_queue.get_nowait()
                self.logger.info('send msg to ros: ' + str(msg_data))
                self.send_msg_ros(msg_data)
            time.sleep(0.05)

    def __init_callback(self):
        # 内部处理函数初始化
        self.callback_dict['snap_req'] = self.snap_callback
        self.callback_dict['send_info_req'] = self.send_info_req_callback
        self.callback_dict['progress_notify'] = self.progress_callback

        # 模块间通信函数初始化
        self.subscribe_msg(self.msg_id.interface_ros_send_msg_out, self.interface_ros_send_msg_out)

    def progress_callback(self, data):
        self.send_mode_mode_working_progress_notify(data)
        pass

    def send_mode_mode_working_progress_notify(self, data):
        self.logger.info('receive process ' + str(data))
        msg_data = {}
        if 'progress_percent' in data:
            msg_data['progress_percent'] = data['progress_percent']
        self.send_msg_dispatcher(self.msg_id.mode_mode_working_progress_notify, msg_data)

    def snap_callback(self, data):
        if data:
            pass
        self.send_msg_dispatcher(self.msg_id.snap_req)
        return

    def send_base_frame_info_notify(self, data):
        msg_data = {}

        if 'voltage_percent' in data:
            msg_data['voltage_percent'] = data['voltage_percent']

        if 'yewei2_percent' in data:
            msg_data['yewei2_percent'] = data['yewei2_percent']

        if 'Position_X' in data and 'Position_Y' in data:
            msg_data['Position_X'] = data['Position_X']
            msg_data['Position_Y'] = data['Position_Y']

        self.send_msg_dispatcher(self.msg_id.base_frame_info_notify, msg_data)
        return

    def send_ui_manager_robot_status(self, data):
        msg_data = {}
        if 'robot_status' in data:
            if data['robot_status'] == 'mt' or data['robot_status'] == 'at':
                msg_data['robot_status'] = data['robot_status']
        self.send_msg_dispatcher(self.msg_id.ui_manager_robot_status_notify, msg_data)
        return

    def send_mode_mt_update_button_status(self, data):
        msg_data = {}
        if 'brush_status' in data:
            msg_data['brush_status'] = data['brush_status']

        if 'water_status' in data:
            msg_data['water_status'] = data['water_status']

        if 'direction_status' in data:
            msg_data['direction_status'] = data['direction_status']

        self.send_msg_dispatcher(self.msg_id.mode_mt_update_button_status, msg_data)
        return

    def send_info_req_callback(self, data):
        self.received_time = time.time()
        # 处理信息 分发到 ui_manager base_frame mode_mt
        self.send_base_frame_info_notify(data)
        self.send_ui_manager_robot_status(data)
        self.send_mode_mt_update_button_status(data)
        return

    def interface_ros_send_msg_out(self, data_dict):
        _, msg_data = Util.get_msg_id_data_dict(data_dict)
        if msg_data is not None and isinstance(msg_data, dict):
            if self.ros_is_running:
                if self.ui_ros_topic_is_sub:
                    # self.send_msg_ros(msg_data)
                    self.msg_out_queue.put_nowait(msg_data)
                else:
                    self.logger.info('/ui_ros_topic is not Subscriber')
            else:
                self.logger.info('ros_master is not run')
        return

    def send_msg_ros(self, msg_data):
        ret, send_msg = Util.dict_to_ros_msg(msg_data)
        if ret == 'ok':
            self.pub.publish(send_msg)
        else:
            self.logger.warning('msg : ' + str(msg_data) + 'to json fail by:' + str(ret))
        return

    def start(self):
        Util.add_thread(target=self.__run)
        return

    def __run(self):
        self.logger.info(self.module_name + ' is started, wait for roscore start')
        while not self.ros_is_running:
            time.sleep(1)

        self.logger.info('roscore init success! init sub pub.')
        self.__init_sub_pub()
        time.sleep(5)
        self.__main_logic()
        return

    def send_msg_link_status(self, status):
        msg_data = {'link_ros': status, 'link_mcu': status}
        self.send_msg_dispatcher(self.msg_id.base_frame_update_link_status, msg_data)
        self.send_msg_dispatcher(self.msg_id.mode_mt_update_link_status, msg_data)
        return

    def check_ui_ros_topic_is_sub(self):
        pubs, subs, _ = self.master.getSystemState()
        ui_ros_topic_is_sub = False
        for index in subs:
            if '/ui_ros_topic' in index:
                ui_ros_topic_is_sub = True
        self.ui_ros_topic_is_sub = ui_ros_topic_is_sub
        return

    def __main_logic(self):
        self.master = Master('/rostopic')
        check_cnt = 0
        self.logger.info('begin start __main_logic')
        while not rospy.is_shutdown():
            check_cnt += 1
            if check_cnt == 5:
                check_cnt = 0
                self.check_ui_ros_topic_is_sub()
            if time.time() - self.received_time < 1:
                self.link_mcu = True
                self.link_ros = True
            else:
                self.link_mcu = False
                self.link_ros = False

            if self.send_link_status != self.link_ros:
                self.logger.info('send link ros : ' + str(self.link_ros))
                self.send_link_status = self.link_ros
                self.send_msg_link_status(self.link_ros)
                time.sleep(1)
                self.send_msg_dispatcher(self.msg_id.mode_start_status,
                                         {'index': setting.start_xiaoyuan, 'status': self.link_ros})

            time.sleep(1)

        self.logger.info('end start __main_logic')
        return

    def __init_sub_pub(self):
        self.pub = rospy.Publisher('/ui_ros_topic', String, queue_size=100)
        rospy.Subscriber('/ros_ui_topic', String, self.callback)
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.amcl_pose_callback)
        return

    def amcl_pose_callback(self, pose:PoseWithCovarianceStamped):
        amcl_x = pose.pose.pose.position.x
        amcl_y = pose.pose.pose.position.y
        # self.logger.info('receive_position x:' + str(amcl_x) + ' y:' + str(amcl_y))
        msg_data = {'x': amcl_x, 'y': amcl_y, 'z': 0}
        self.send_msg_dispatcher(self.msg_id.mode_working_position_notify, msg_data)

    def send_ack_callback(self, msg_id, msg_type):
        msg_data = {'msg_id': msg_id, 'msg_type': msg_type}
        self.send_msg_ros(msg_data)
        return

    def callback(self, data):
        ret, data_dict = Util.ros_msg_to_dict(data)
        if ret == 'ok' and data_dict is not None:
            if 'msg_id' in data_dict and 'msg_type' in data_dict:

                msg_id = data_dict['msg_id']
                msg_type = data_dict['msg_type']
                msg_data = ''

                if '_ack' not in msg_id:
                    self.send_ack_callback(msg_id + '_ack', msg_type)

                if 'msg_data' in data_dict:
                    msg_data = data_dict['msg_data']

                callback = self.callback_dict.get(msg_id)
                if callback is not None:
                    callback(msg_data)
        else:
            self.logger.warning(str(data_dict) + '--- msg errer : ' + str(ret))
        return

    def init_ros_node(self):
        roslaunch.rlutil._wait_for_master()
        self.logger.info('roscore inited!!')
        time.sleep(1)

        rospy.init_node('ros_ui_start', anonymous=True)

        self.ros_is_running = True
        return
