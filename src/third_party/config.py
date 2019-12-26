import os
import configparser


def get_value_by_key(key, section):
    print('config get key:' + str(key) + ' section:' + str(section))
    config = Config()
    return config.get_value_by_key(key, section)


class Config(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join(os.environ['HOME'] + '/release/config/config.ini')
        self.config.read(self.config_path)
        self.init_config()

    def init_config(self):

        if not os.path.isfile(self.config_path):
            print('no config.ini existed, create!')
            if not os.path.isdir(self.config_path.strip('config.ini')):
                os.system('mkdir -p ' + self.config_path.strip('config.ini'))
            os.system('touch ' + self.config_path)
            self.set_default_config()

    def set_default_config(self):
        # 版本
        self.config.add_section('VERSION')
        self.config.set('VERSION', 'version', 'U_V0.0.1')
        # 序列号
        self.config.add_section('SN')
        self.config.set('SN', 'sn', 'U12345678')
        # launch文件配置
        self.config.add_section('LAUNCH')
        self.config.set('LAUNCH', 'underpan',
                        '/home/utry/catkin_ws/src/xiaoyuan_robot_v2/launch/xiaoyuan_robot_start_underpan.launch')

        self.config.set('LAUNCH', 'other',
                        '/home/utry/catkin_ws/src/xiaoyuan_robot_v2/launch/xiaoyuan_robot_start_other.launch')

        self.config.set('LAUNCH', 'linerunning',
                        '/home/utry/catkin_ws/src/linerunning_v2/launch/xiaoyuan_clear.launch')
        # 本机配置
        self.config.add_section('DATA_PATH')
        self.config.set('DATA_PATH', 'database', self.config_path.strip('config.ini'))
        # 本机配置
        self.config.add_section('HOST_URL')
        self.config.set('HOST_URL', 'qrcode_download_url', 'http://47.100.182.145:8080/qrcode/clearQrcode?macId=')
        self.config.set('HOST_URL', 'unlock_url', 'http://47.100.182.145:8080/lock/queryUnlockById?macId=')
        self.config.set('HOST_URL', 'lock_url', 'http://47.100.182.145:8080/lock/lock?macId=')
        self.config.set('HOST_URL', 'update_url', 'http://47.100.182.145:9200/update_info?')
        self.config.set('HOST_URL', 'update_download_url', 'http://47.100.182.145:9200')
        # 本机配置
        self.config.add_section('CONFIG')
        self.config.set('CONFIG', 'password', '889972')
        self.config.set('CONFIG', 'encrypted', 'no')
        self.config.set('CONFIG', 'video_record_enable', 'yes')
        self.config.set('CONFIG', 'video_record_time', '180')  # 单位s
        self.config.set('CONFIG', 'video_record_size', '1024')  # 单位m
        self.config.set('CONFIG', 'video_record_flip', 'yes')  # 是否需要翻转
        self.config.set('CONFIG', 'check_memory', 'no')  # 是否需要检测内存泄露
        self.config.set('CONFIG', 'rtmp_enable', 'no')  # 是否需要开启rtmp推流
        self.config.set('CONFIG', 'rtmp_url', 'rtmp://120.26.209.2:1935/live/test')  # rtmp
        self.config.set('CONFIG', 'http_local_enable', 'no')  # 本地服务器

        with open(self.config_path, 'w') as f_config:
            self.config.write(f_config)

    def get_value_by_key(self, key, section):
        res = None
        self.config.read(self.config_path)
        if self.config.has_section(section):
            if self.config.has_option(section,key):
                res = self.config.get(section, key)
        return res


# test code
if __name__ == '__main__':
    config = Config()
    print(config.get_value_by_key('rtmp_url', 'CONFIG'))
