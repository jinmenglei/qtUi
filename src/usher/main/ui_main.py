import sys
path_src = '/home/utry/PycharmProjects/qtUi/'
sys.path.append(path_src)
path_top = '/home/utry/PycharmProjects/qtUi/src/'
sys.path.append(path_top)
print(sys.path)
from usher.manager.manager import Manager


if __name__ == '__main__':
    manager = Manager()
    manager.start()
