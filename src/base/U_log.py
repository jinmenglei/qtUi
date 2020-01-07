# logconfig file

import logging
from logging.handlers import RotatingFileHandler
import os


level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'crit': logging.CRITICAL
}  # 日志级别关系映射


log_module_dict = {}
log_pid_lock_dict = {}


def get_logger(name='root', filename='utry_log.log', level='info', max_bytes=10 * 1024 * 1024, filecount=40):
    print(' before 真是不信了！！！！ ' + str(logging._lock) + ' ' + str(name))
    my_pid = os.getpid()
    if log_pid_lock_dict.get(my_pid) is None:
        log_pid_lock_dict[my_pid] = logging._lock
        try:
            logging._releaseLock()
        except Exception as e:
            print('try to release :' + str(e))

    logger = log_module_dict.get(name)
    if logger is None:
        logger = logging.getLogger(name)
        logger.setLevel(level=level_relations[level])
        log_path = os.path.join(os.environ['HOME'] + '/release/log', filename)

        log_dir = os.environ['HOME'] + '/release/log'
        if not os.path.isdir(log_dir):
            os.system('mkdir -p ' + log_dir)
            # os.mkdir(os.environ['HOME'] + '/release/log')

        formatter = logging.Formatter('%(asctime)s - %(levelname)7s - %(message)s - %(name)s')

        file_handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=filecount)
        file_handler.setLevel(level=level_relations[level])
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        shell_handler = logging.StreamHandler()
        shell_handler.setFormatter(formatter)
        shell_handler.setLevel(level=level_relations[level])
        logger.addHandler(shell_handler)

        log_module_dict[name] = logger

    return logger


class logger_inner:
    def info(log: str):
        print(log)
        pass

    def warning(log: str):
        print(log)
        pass

    def debug( log: str):
        print(log)
        pass

    def error(log: str):
        print(log)
        pass

    def critical(log: str):
        print(log)
        pass

    def fatal(log: str):
        print(log)
        pass


"""test code"""
if __name__ == '__main__':
    logger = get_logger('test')
    logger.info('info')
    logger.debug('debug')
    logger.warning('warn')
    logger.fatal('fatal')
    logger.critical('critical')
