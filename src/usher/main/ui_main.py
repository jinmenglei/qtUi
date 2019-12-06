import sys
path_src = '/home/utry/PycharmProjects/qtUi/'
sys.path.append(path_src)
path_top = '/home/utry/PycharmProjects/qtUi/src/'
sys.path.append(path_top)
print(sys.path)
from usher.manager.manager import Manager
# from xml.etree.cElementTree import parse


if __name__ == '__main__':
    # xml_fd = open('/home/utry/catkin_ws/src/xiaoyuan_robot_v2/launch/xiaoyuan_robot_start_amcl.launch')
    # et = parse(xml_fd)
    # root = et.getroot()
    # print(root)
    # for child in root:
    #     print(child)
    #     for sub_child in child:
    #         print(sub_child)
    #
    # dom = parse('/home/utry/catkin_ws/src/xiaoyuan_robot_v2/launch/xiaoyuan_robot_start_amcl.launch')
    # arg = dom.ge
    # pass
    manager = Manager()
    manager.start()
