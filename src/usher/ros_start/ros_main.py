import sys
# path_src = '/home/utry/PycharmProjects/qtUi/'
# sys.path.append(path_src)
# path_top = '/home/utry/PycharmProjects/qtUi/src/'
# sys.path.append(path_top)
print(sys.path)
from usher.ros_start.ros_manager import RosManager


if __name__ == '__main__':
    manager = RosManager()
    manager.start()


