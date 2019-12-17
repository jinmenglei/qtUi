# do something here
import json
from std_msgs.msg import String
import os
import uuid
from threading import Thread
import hashlib


def get_map_num():
    data_bag = os.environ['HOME'] + '/catkin_ws/src/databag/'
    map_list = []
    # 判断是否有databag文件夹
    if not os.path.isdir(data_bag):
        pass
    else:
        # 拉出所有文件
        file_list = os.listdir(data_bag)
        # 按照创建时间排序
        file_list = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(data_bag, x)), reverse=True)
        # 拿出pcd文件
        list_pcd = []
        list_png = []
        for file in file_list:
            if '.pcd' in str(file):
                list_pcd.append(file)
            if '.png' in file:
                list_png.append(file)
        # 拿出有waypoint文件的pcd

        for pcd in list_pcd:
            name = str(pcd).strip('.pcd')
            csv_name = name+'wp.csv'
            if csv_name not in file_list:
                list_pcd.remove(pcd)

        # 组装下返回值
        for pcd in list_pcd:
            png_path = ':/mode_map_select/mode_map_select/default.png'
            name = str(pcd).strip('.pcd')
            for png in list_png:
                if str(pcd).strip('.pcd') in png:
                    png_path = data_bag + png

                    tmp_name = str(png).strip('.png').strip((str(pcd).strip('.pcd')) + '_')
                    if tmp_name != '':
                        name = tmp_name
                    break
            tmp_dict = {'pcd': data_bag + pcd, 'wp': data_bag + str(pcd).strip('.pcd') + 'wp.csv', 'png': png_path,
                        'name': name}
            map_list.append(tmp_dict)
    return map_list

def get_md5sum(filename):
    block_size = 64*1024
    md5 = hashlib.md5()
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            while True:
                content = f.read(block_size)
                if not content:
                    break
                md5.update(content)
                return 'ok', md5.hexdigest()

    else:
        return 'file ' + filename + ' is not existed', 0


def do_restart():
    os.system('reboot')


def get_mac_address():
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac


def get_uuid() -> str:
    return str(uuid.uuid4())


def add_thread(target=None, name=None, args=(), kwargs=None, *, daemon=None):
    task = Thread(target=target,)
    task.start()
    return task


def json_to_dict(json_str) -> (str, dict):
    try:
        dict_ret = json.loads(json_str)
        return 'ok', dict_ret
    except json.JSONDecodeError as e:
        return e, {}


def ros_msg_to_dict(ros_data) -> (str, dict):
    return json_to_dict(ros_data.data)


def dict_to_json(dict_data) -> (str, dict):
    try:
        json_str = json.dumps(dict_data)
        return 'ok', json_str
    except json.JSONDecodeError as e:
        return e, {}


def get_res_path(mode_name) -> str:
    path = os.path.join(os.environ['HOME'] + '/release/res/', mode_name+'/')
    if not os.path.isdir(path):
        os.system('mkdir -p ' + path)
    return path


def dict_to_ros_msg(dict_data) -> (str, String):
    send_msg = String()
    ret, json_str = dict_to_json(dict_data)

    send_msg.data = str(json_str)
    return ret, send_msg


def get_msg_id_data_dict(data_dict) -> (str, dict):
    msg_id = None
    msg_data = {}
    if isinstance(data_dict, dict):
            msg_id = data_dict.get('msg_id')
            msg_data = data_dict.get('msg_data')

    return msg_id, msg_data


def get_index_tip_msg_data(msg_data) -> (int, str):
    index = None
    tip = ''
    if isinstance(msg_data, dict):
        index = msg_data.get('index')
        tip = msg_data.get('tip')
        if not isinstance(index, int):
            index = None
    return index, tip


def get_msg_id_from_data_dict(data_dict) -> (str,str):
    error_code = 'ok'
    msg_id = ''
    if isinstance(data_dict, dict):
        if 'msg_id' in data_dict:
            msg_id = data_dict['msg_id']
        else:
            error_code = str(data_dict) + ' --- type error, no msg_id'
    else:
        error_code = str(data_dict) + ' --- type error, need dict!'

    return error_code, msg_id


# test code
if __name__ == '__main__':
    print(get_map_num())