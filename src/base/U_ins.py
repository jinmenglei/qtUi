"""
message instance for model,this record info
"""
from base.U_log import get_logger


class Ins(object):
    __instance = None
    """init first"""
    __first = True

    def __init__(self):
        if self.__first:
            self.__first = False
            self.__module_queue_dict = {}
            self.__logger = get_logger('pyins')
            pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance:
            return cls.__instance
        else:
            obj = object.__new__(cls, *args, **kwargs)
            cls.__instance = obj
            return cls.__instance

    def add_module_queue(self, module_name, queue):
        self.__logger.info('add :' + str(module_name) + ' to queue: ' + str(queue))
        self.__module_queue_dict[module_name] = queue

    def delete_module(self, module_name):
        if module_name in self.__module_queue_dict:
            self.__module_queue_dict.pop(module_name)
            self.__logger.info('delete ' + str(module_name) + ' success!')
        else:
            self.__logger.info('delete fail ' + str(module_name) + ' not add !')

    def get_queue_by_module_name(self, module_name):
        return self.__module_queue_dict.get(module_name)


"""test code"""
if __name__ == '__main__':
    for index in range(10):
        ins0 = Ins()
        print(ins0)
    pass
