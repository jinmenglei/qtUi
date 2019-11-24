#!/usr/bin/env python
# encoding: utf-8
# module ui.setting
# config all the ui
# no doc
from PyQt5.QtCore import QRect

# version info
versionMajor = 0
versionMinor = 0
versionDev = 1

date = '2019.10.09'


def get_version_date():
    return date


def get_version_detail():
    return versionMajor, versionMinor, versionDev

# version info


master_node, slave_node = range(2)
download_idle, downloading, download_ok, download_fail = range(4)
update_idle, update_base, update_head, update_move, update_ui = range(5)
# class PageMode:
#     """这个是页面的模式类"""

Label_title_4G, Label_title_time, Lable_title_mode_select, Label_title_battery = range(4)
Label_tail_water_percent, Label_tail_water_name,  Label_tail_odom_percent, Label_tail_odom_name = range(4)

Title_index_name, Title_index_point, Title_index_font_size, Title_index_border = range(4)
# 这个字典保存着初始化的位置和属性等等
list_title_string = [
    ['4G', QRect(50, 11, 29, 18), 16, 90],
    ['08:08', QRect(90, 11, 70, 18), 16, 90],
    ['模式选择', QRect(345, 5, 108, 30), 20, 90],
    ['88%', QRect(680, 11, 60, 18), 16, 90]
]

list_tail_string = [
    ['88%', QRect(115, 19, 70, 25), 21, 90],
    ['水量', QRect(120, 55, 59, 30), 21, 90],
    ['88%', QRect(658, 19, 120, 25), 21, 90],
    ['里程', QRect(676, 55, 59, 30), 21, 90]
]
# add panel index
Page_mt_mode, Page_author, Page_check, Page_map_select, Page_working, Page_show_box, Page_Update, Page_num = range(8)  # 6个页面
Page_index_title, Page_index_tail = range(2)  # 显示索引
# 这个是标题和提示显示的内容
list_page_string = [
    ['手动模式', ''],
    ['验证鉴权', '请扫描二维码或\n输入管理员密码'],
    ['自检中', ''],
    ['地图选择', '请点击所要清扫\n的区域地图'],
    ['工作中',   '自动驾驶工作中\n请勿操作！'],
    ['升级中',   '自动驾驶工作中\n请勿操作！'],
    ['升级中',   '自动驾驶工作中\n请勿操作！']
]

Mt_button_off, Mt_button_on, Mt_button_point, Mt_button_id = range(4)
Mt_brush_button, Mt_water_button, Mt_direction_button, Mt_button_num = range(4)
list_label_info, list_label_point, list_label_size = range(3)

Mt_brush_id, Mt_water_id, Mt_direction_id = range(10010, 10010 + 3)
Mt_button_id_delta = 10010
Mt_button_forward, Mt_button_back = range(2)
list_button_mt_string = [
    ['滑条-灰.png', '滑条-蓝.png', QRect(85, 121, 206, 106), Mt_brush_id],
    ['滑条-灰.png', '滑条-蓝.png', QRect(344, 121, 206, 106), Mt_water_id],
    ['前进.png', '后退.png', QRect(593, 120, 108, 206), Mt_direction_id]
]

list_label_mt_string = [
    ['刷盘', QRect(170, 69, 60, 30)],
    ['吸水', QRect(430, 69, 60, 30)],
    ['方向', QRect(620, 69, 60, 30)],
]

Author_radio_off, Author_radio_on, = range(2)
list_radio_author_string = [
    '未输入.png', '输入.png'
]

Author_button_id_delta = 10086
Author_button_id_0, Author_button_id_1, Author_button_id_2, Author_button_id_3, Author_button_id_4, \
    Author_button_id_5, Author_button_id_6, Author_button_id_7, Author_button_id_8, Author_button_id_9, \
    Author_button_id_delete, Author_button_id_clear = range(Author_button_id_delta, Author_button_id_delta + 12)

Author_button_unselect, Author_button_select, Author_button_point, Author_button_id = range(4)
list_button_author_info = [
    ['0.png', '0-选中.png', QRect(192, 109, 90, 90), Author_button_id_0],
    ['1.png', '1-选中.png', QRect(288, 109, 90, 90), Author_button_id_1],
    ['2.png', '2-选中.png', QRect(384, 109, 90, 90), Author_button_id_2],
    ['3.png', '3-选中.png', QRect(480, 109, 90, 90), Author_button_id_3],
    ['4.png', '4-选中.png', QRect(576, 109, 90, 90), Author_button_id_4],
    ['5.png', '5-选中.png', QRect(192, 205, 90, 90), Author_button_id_5],
    ['6.png', '6-选中.png', QRect(288, 205, 90, 90), Author_button_id_6],
    ['7.png', '7-选中.png', QRect(384, 205, 90, 90), Author_button_id_7],
    ['8.png', '8-选中.png', QRect(480, 205, 90, 90), Author_button_id_8],
    ['9.png', '9-选中.png', QRect(576, 205, 90, 90), Author_button_id_9],
    ['删除.png', '删除-选中.png', QRect(672, 109, 90, 90), Author_button_id_delete],
    ['清除.png', '清除-选中.png', QRect(672, 205, 90, 90), Author_button_id_clear],
]

list_working_name, list_working_point, list_working_size = range(3)
list_working_label_info = [
    ['进度', QRect(290, 37, 53, 26)],
    ['速度', QRect(290, 88, 53, 26)],
    ['效率', QRect(290, 139, 53, 26)],
    ['坐标', QRect(290, 189, 53, 26)]
]
list_working_format_string = ['{:3d}','{:3.2f}','{:3d}']

list_working_gray_point, list_working_text_point = range(2)
list_working_process_info = [
    [QRect(358, 32, 380, 38), QRect(490, 32, 120, 38)],
    [QRect(358, 86, 380, 38), QRect(490, 86, 120, 38)],
    [QRect(358, 137, 380, 38), QRect(490, 137, 120, 38)],
]
list_working_label_unit = ['%', 'm/s', 'm²/h']
list_working_max_value = [100, 1, 100]
Working_gauge_progress, Working_gauge_speed, Working_gauge_efficiency, Working_gauge_num = range(4)
Working_point_x, Working_point_y, Working_point_z, Working_point_num = range(4)
list_working_label_point = ['X:', 'Y:', 'Z:']

Map_button_id_delta = 10000
Map_select_1, Map_select_2, Map_select_3, Map_select_4, Map_select_5, Map_select_6, Map_select_7, Map_select_8, \
    Map_select_num = range(9)
Map_select_id1, Map_select_id2, Map_select_id3, Map_select_id4, Map_select_id5, Map_select_id6, Map_select_id7,\
    Map_select_id8 = range(Map_button_id_delta, Map_button_id_delta + 8)

Map_button_path, Map_button_id, Map_button_point, Map_label_string, Map_label_point, Map_back_point = range(6)
list_button_map_string = [
    ['map1.pgm', Map_select_id1, QRect(100, 10, 120, 120), '地图1', QRect(100, 139, 120, 26), QRect(97, 7, 126, 126),],
    ['map2.pgm', Map_select_id2, QRect(260, 10, 120, 120), '地图2', QRect(260, 139, 120, 26), QRect(257, 7, 126, 126)],
    ['map3.pgm', Map_select_id3, QRect(420, 10, 120, 120), '地图3', QRect(420, 139, 120, 26), QRect(417, 7, 126, 126)],
    ['map4.pgm', Map_select_id4, QRect(580, 10, 120, 120), '地图4', QRect(580, 139, 120, 26), QRect(577, 7, 126, 126)],
    ['map5.pgm', Map_select_id5, QRect(100, 178, 120, 120), '地图5', QRect(100, 307, 120, 26), QRect(97, 175, 126, 126)],
    ['map6.pgm', Map_select_id6, QRect(260, 178, 120, 120), '地图6', QRect(260, 307, 120, 26), QRect(257, 175, 126, 126)],
    ['map7.pgm', Map_select_id7, QRect(420, 178, 120, 120), '地图7', QRect(420, 307, 120, 26), QRect(417, 175, 126, 126)],
    ['map8.pgm', Map_select_id8, QRect(580, 178, 120, 120), '地图8', QRect(580, 307, 120, 26), QRect(577, 175, 126, 126)]
]

check_panel_size = 380
Check_tip_link, Check_tip_status, Check_tip_num = range(3)
Check_title, Check_content_subtitle, Check_content_function, Check_content_result_info = range(4)
Check_content_result_NG, Check_content_result_PASS = range(2)
Check_4g, Check_ros, Check_mcu, Check_battery, Check_water, Check_release_stop, Check_fault, Check_origin = range(8)
Check_status_idle, Check_status_checking, Check_status_pass, Check_status_ng = range(4)

check_list_all = [
    ['连接检测', '4G', None, ['未连接', '已连接']],
    ['连接检测', 'ROS', None, ['未连接', '已连接']],
    ['连接检测', 'MCU', None, ['未连接', '已连接']],
    ['状态检测', '电量', None, ['电量不足', '电量充足']],
    ['状态检测', '水位', None, ['水量过低', '水量正常']],
    ['状态检测', '急停', None, ['未释放', '已释放']],
    ['状态检测', '故障检测', None, ['有故障', '无故障']],
    ['状态检测', '原点检测', None, ['不在原点', '在原点']]
]

Update_download, Update_md5, Update_unzip, Update_base, Update_move, Update_ui, Update_cnt = range(7)
Update_status_idle, Update_status_checking, Update_status_pass, Update_status_ng = range(4)
Update_title, Update_subtitle, Update_function, Update_result_status, Update_process = range(5)

Update_list_all = [
    ['下载升级包', '进度', None, Update_status_idle, 0],
    ['完整性校验', '状态', None, Update_status_idle, 0],
    ['解压升级包', '状态', None, Update_status_idle, 0],
    ['升级主控', '进度', None, Update_status_idle, 0],
    ['升级导航', '进度', None, Update_status_idle, 0],
    ['升级界面', '进度', None, Update_status_idle, 0],
]


show_box_tip, show_box_point, show_box_yes, show_box_no = range(4)
show_box_turn_mt, show_box_turn_at, show_box_map_select, show_box_work_cancel, show_box_loss, show_box_update, \
    show_box_no_map = range(7)
list_show_box_string = [
    ['是否要切换为\n 手动驾驶模式', QRect(173, 158, 438, 50), Page_mt_mode, None],
    ['是否要切换为\n 自动驾驶模式', QRect(173, 158, 438, 50), Page_author, None],
    ['是否开始清扫', QRect(258, 123, 279, 100), Page_working, None],
    ['是否要取当前任务，\n并且切换到手动驾驶？', QRect(227, 129, 380, 100), Page_mt_mode, None],
    ['失去底层连接\n 请联系售后', QRect(227, 129, 380, 100), None, None],
    ['检测到新版本\n 是否升级', QRect(227, 129, 380, 100), Page_Update, None],
    ['地图不存在或不可用\n 是否重新选择', QRect(227, 129, 380, 100), Page_map_select, Page_mt_mode],
]
