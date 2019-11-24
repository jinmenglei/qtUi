# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import image_rc
import sys


class Ui_Form(object):
    def setupUi(self, Form):
        # Form.setObjectName("Form")
        Form.resize(800, 480)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.frame.setStyleSheet("background-color: rgb(214, 213, 214);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        # self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 800, 40))
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_2.setObjectName("frame_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(13, 12, 28, 17))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/frame/res/frame/信号4.png"))
        # self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(50, 11, 29, 18))
        font = QtGui.QFont()
        font.setFamily("MicrosoftYaHei")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 16pt \"MicrosoftYaHei\";")
        self.label_2.setText("4G")
        # self.label_2.setObjectName("label_2")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(0, 380, 800, 100))
        self.frame_3.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setLineWidth(0)
        # self.frame_3.setObjectName("frame_3")
        self.pushButton = QtWidgets.QPushButton(self.frame_3)
        self.pushButton.setGeometry(QtCore.QRect(235, 0, 331, 100))
        self.pushButton.setStyleSheet("border-image: url(:/frame/res/frame/切换到 自动驾驶.png);")
        self.pushButton.setText("")
        # self.pushButton.setObjectName("pushButton")

        # self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.__init_connet()

    def __init_connet(self):
        self.pushButton.clicked.connect(lambda :self.pushButton.setStyleSheet(
            "border-image: url(:/frame/res/frame/切换到 手动驾驶.png);"))

    # def retranslateUi(self, Form):
    #     _translate = QtCore.QCoreApplication.translate
    #     Form.setWindowTitle(_translate("Form", "Form"))
    #


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = QtWidgets.QWidget()
    widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    widget.move(0, 0)
    ui_manager = Ui_Form()
    ui_manager.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())