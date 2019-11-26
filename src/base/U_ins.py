"""
这个是最基础的类,一个线程只会初始化一次,
这里面保存着模块和通信接口的对应关系
"""
from base.U_log import get_logger


class Ins(object):
    __instance = None
    """init first"""
    __first = True

    def __init__(self):
        if self.__first:
            # 单例模式
            self.__first = False
            # 模块和接口对应关系,现在用的Queue,我可能会变
            self.__module_queue_dict = {}
            #初始化logger模块
            self.__logger = get_logger('pyins')
            pass

    def __new__(cls, *args, **kwargs):
        """
        实例操作
        :param args:
        :param kwargs:
        :return:
        """
        if cls.__instance:
            return cls.__instance
        else:
            obj = object.__new__(cls, *args, **kwargs)
            cls.__instance = obj
            return cls.__instance

    def add_module_queue(self, module_name, queue):
        """
        存对应关系
        :param module_name:
        :param queue:
        :return:
        """
        self.__logger.info('add :' + str(module_name) + ' to queue: ' + str(queue))
        self.__module_queue_dict[module_name] = queue

    def delete_module(self, module_name):
        """
        删除对应关系
        :param module_name:
        :return:
        """
        if module_name in self.__module_queue_dict:
            self.__module_queue_dict.pop(module_name)
            self.__logger.info('delete ' + str(module_name) + ' success!')
        else:
            self.__logger.info('delete fail ' + str(module_name) + ' not add !')

    def get_queue_by_module_name(self, module_name):
        """
        获取对应模块的通信接口
        :param module_name:
        :return:
        """
        return self.__module_queue_dict.get(module_name)


# test code
if __name__ == '__main__':
    for index in range(10):
        ins0 = Ins()
        print(ins0)
    pass
