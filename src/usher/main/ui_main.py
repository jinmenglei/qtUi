import sys
import os
path_src = os.path.abspath('../../')
sys.path.append(path_src)
path_top = os.path.abspath('../../../')
sys.path.append(path_top)
print(sys.path)
from usher.manager.manger import Manager


if __name__ == '__main__':
    manager = Manager()
    manager.start()
