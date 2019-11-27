from base.U_app import App
from PyQt5.QtWidgets import QFrame, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QRect, Qt, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QPixmap, QMovie, QFont
import time


def get_sub_frame(parent, geometry=QRect(0, 0, 800, 480), style_sheet='', need_shape=False):
    """
    初始化一个子frane
    :param parent:
    :param geometry:位置大小
    :param style_sheet:样式,主要是透明背景啥的
    :param need_shape:需要外边框不
    :return:Qframe 实例
    """
    frame = QFrame(parent)
    frame.setGeometry(geometry)
    frame.setStyleSheet(style_sheet)
    if not need_shape:
        frame.setFrameShape(QFrame.NoFrame)

    return frame


def get_pushbutton(parent, geometry=QRect(0, 0, 800, 480), style_sheet='', text=''):
    """
    一个神奇的按钮
    :param parent:
    :param geometry:位置大小
    :param style_sheet: 主要是背景图
    :param text: 文字显示
    :return: 按钮实例
    """
    push_button = QPushButton(parent)
    push_button.setGeometry(geometry)
    push_button.setStyleSheet(style_sheet)
    push_button.setText(text)

    return push_button


def get_label_text(parent, geometry=QRect(0, 0, 800, 480), bold=False, text='',
                   font_px=20, font_family='MicrosoftYaHei', font_color='#000000'):
    """
    获取一个文字label实例
    :param parent:
    :param geometry: 位置大小
    :param bold: 加粗
    :param text: 文字
    :param font_px: 大小
    :param font_family:字体
    :param font_color: 颜色
    :return: Qlabel实例
    """
    label = QLabel(parent)
    label.setGeometry(geometry)
    label.setText(text)
    label.setAlignment(Qt.AlignCenter)

    style_sheet = 'QLabel{color: ' + font_color + '}'

    font = QFont()
    font.setFamily(font_family)
    font.setPixelSize(font_px)
    # font.setBold(bold)
    if bold:
        font.setWeight(70)
    label.setFont(font)

    label.setStyleSheet(style_sheet)

    return label


def get_label_picture(parent, geometry=QRect(0, 0, 800, 480), picture_path=None):
    """
    获取一个图片Qlabel实例
    :param parent:
    :param geometry: 位置大小
    :param picture_path: 图片路径
    :param is_gif: 是不是gif
    :return: Qlabel实例
    """
    label = QLabel('', parent)
    label.setGeometry(geometry)
    if picture_path is not None:
        if '.gif' in picture_path:
            movie = QMovie(picture_path)
            label.setMovie(movie)
            movie.start()
        else:
            label.setPixmap(QPixmap(picture_path).scaled(label.width(), label.height()))

    return label


class MultiThread(QThread):
    multi_signal = pyqtSignal(dict)

    def __init__(self, multi_pipe):
        QThread.__init__(self)
        self.multi_pipe = multi_pipe

    def run(self):
        while not self.__is_shutdown:
            data_dict = self.multi_pipe.recv()
            self.multi_signal.emit(data_dict)

            time.sleep(0.0001)


class App_Qobject(QObject, App):
    qt_signal = pyqtSignal(dict)

    def __init__(self, module_name):
        App.__init__(self, module_name)
        self.multi_thread = None
        # self.__start__()

    def __init_thread_connect(self):
        self.__queue = self.qt_signal
        self.__queue.connect(self.__deal_data_dict)

    def __start__(self):
        """
        rewrite for qt
        :return:
        """
        if self.__pipe_dispatcher_rec is not None:
            self.multi_thread = MultiThread(self.__pipe_dispatcher_rec)
            self.multi_thread.multi_signal.connect(self.__slot_multi_callbac)
            self.multi_thread.start()

    def __slot_multi_callback(self, data_dict):
        if self.__multi_default_callback is not None:
            self.__multi_default_callback(data_dict)

    def send_msg_inner(self, send_queue, data_dict):
        if isinstance(send_queue, pyqtSignal):
            print('tests')
            send_queue.emit(data_dict)



class Q_App(App_Qobject, QFrame):
    """这个是界面的基础类,包含通讯和基本控件设置"""
    start_signal = pyqtSignal()
    stop_signal = pyqtSignal()

    def __init__(self, module_name, parent=None, geometry=QRect(0,0,800,480), style_sheet=''):
        App.__init__(self, module_name)
        QFrame.__init__(self, parent=parent)
        self.setGeometry(geometry)
        self.setStyleSheet(style_sheet)
        self.start_signal.connect(lambda: self.start())
        self.stop_signal.connect(lambda: self.stop())

    def start(self):
        """
        test timer
        :return:
        """
        pass

    def stop(self):
        """
        tongshang
        :return:
        """
        pass

    def showEvent(self, QShowEvent):
        """
        重写显示事件,不用外部操作定时器,减少代码
        :param QShowEvent:
        :return:
        """
        self.start_signal.emit()
        QWidget.showEvent(self, QShowEvent)

    def hideEvent(self, QHideEvent):
        """
        重写隐藏事件,同上
        :param QHideEvent:
        :return:
        """
        self.stop_signal.emit()
        QWidget.hideEvent(self, QHideEvent)
