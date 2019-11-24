from base.U_app import App
from PyQt5.QtWidgets import QFrame, QWidget


class Q_App(App, QFrame):
    def __init__(self, module_name, parent=None):
        App.__init__(self, module_name)
        QFrame.__init__(self, parent=parent)

# class Q_App_W(QWidget, App):
#     def __init__(self, module_name, parent=None):
#         QWidget.__init__(self)
#         App.__init__(self, module_name)

