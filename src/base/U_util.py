# do something here
import json
from std_msgs.msg import String
import os
import uuid
from threading import Thread
import hashlib


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
    return os.path.join(os.environ['HOME'] + '/release/res/', mode_name+'/')


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
    x = 'haha'
    print(type(x))
    print(json_to_dict.__annotations__)
    print(json_to_dict('{}'))
    dict_str = {}
    dict_str['msg_id'] = 'xxxx'
    print(dict_to_ros_msg(dict_str))

    print(get_uuid())
    # import time
    # time.sleep(1)
    print(get_uuid())
    print(get_uuid())
    print(get_uuid())
