"""
这里记录着所有的消息，按照模块分类，方便自动联想，
不然谁知道哪个是哪个，还得看文档
"""


class UMsg:
    # dispatcher
    manager_dispatcher = 'manager_dispatcher'
    ui_dispatcher = 'ui_dispatcher'
    service_dispatcher = 'service_dispatcher'
    ros_dispatcher = 'ros_dispatcher'

    manager_register_pipe = 'manager_register_pipe'
    manager_register_msg_id = 'manager_register_msg_id'
    # service_register_msg_id = 'register_msg_id'
    inner_register_id = 'register_msg_id'
    inner_dispatcher = 'dispatcher'
    # self.inner_register_id = None
    out_dispatcher = 'manager_dispatcher'



    # ui_manager
    ui_manager_change_page = 'ui_manager_change_page'
    ui_manager_show_box = 'ui_manager_show_box'
    ui_manager_robot_status_notify = 'ui_manager_robot_status_notify'
    ui_manager_destroy_show_box = 'ui_manager_destroy_show_box'

    # base_frame
    base_frame_info_notify = 'base_frame_info_notify'
    base_frame_set_button_enable = 'base_frame_set_button_enable'
    base_frame_update_link_status = 'base_frame_update_link_status'
    base_frame_update_button_status = 'base_frame_update_button_status'

    # interface_ros
    interface_ros_send_msg_out = 'interface_ros_send_msg_out'

    # videoRecord
    snap_req = 'snap_req'

    # update_task
    update_task_do_process = 'update_task_do_process'

    # mode_mt
    mode_mt_update_button_status = 'mode_mt_update_button_status'
    mode_mt_update_link_status = 'mode_mt_update_link_status'

    # mode_author

    # mode_check

    # mode_map_select

    # mode_working
    mode_working_show_map = 'mode_working_show_map'
    mode_working_speed_notify = 'mode_working_speed_notify'
    mode_working_position_notify = 'mode_working_position_notify'

    # mode_show_box
    mode_show_box_show_tip = 'mode_show_box_show_tip'

    # mode_update
    mode_update_process = 'mode_update_process'
    mode_update_change_result_status = 'mode_update_change_result_status'

    # launch_start
    launch_start_control = 'launch_start_control'


# test code
if __name__ == '__main__':
    print(UMsg.ui_manager_show_box)