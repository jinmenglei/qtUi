from config.setting import *
import wx
import time


class ModeMtPanel(wx.Panel):
    """手动驾驶的panel"""
    def __init__(self, base_frame):
        wx.Panel.__init__(self, base_frame, wx.ID_ANY, wx.Point(0, 40), wx.Size(800, 340))
        base_frame.register_panel(Page_mt_mode, self)
        self.dispatcher = base_frame.dispatcher
        self.mode_dispatcher = base_frame.mode_dispatcher
        self.res_path = '../../res/mode_mt/'

        self.timer_show = wx.Timer(self)  # 创建定时器
        self.Bind(wx.EVT_TIMER, self.on_timer_show, self.timer_show)  # 绑定一个定时器事件

    def start(self):
        self.timer_show.Start(1000)

    def stop(self):
        self.timer_show.Stop()


    def on_timer_show(self, event):
        """标题栏刷新定时器"""

        if event:
            pass
