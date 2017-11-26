# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.host_listview = QtWidgets.QListView(self.centralWidget)
        self.host_listview.setGeometry(QtCore.QRect(0, 0, 151, 301))
        self.host_listview.setObjectName("host_listview")
        self.file_listview = QtWidgets.QListView(self.centralWidget)
        self.file_listview.setGeometry(QtCore.QRect(150, 20, 251, 281))
        self.file_listview.setObjectName("file_listview")
        self.fresh_button = QtWidgets.QPushButton(self.centralWidget)
        self.fresh_button.setGeometry(QtCore.QRect(250, 0, 41, 21))
        self.fresh_button.setObjectName("fresh_button")
        self.back_button = QtWidgets.QPushButton(self.centralWidget)
        self.back_button.setGeometry(QtCore.QRect(150, 0, 41, 21))
        self.back_button.setObjectName("back_button")
        self.forward_button = QtWidgets.QPushButton(self.centralWidget)
        self.forward_button.setGeometry(QtCore.QRect(190, 0, 61, 21))
        self.forward_button.setObjectName("forward_button")
        self.download_button = QtWidgets.QPushButton(self.centralWidget)
        self.download_button.setGeometry(QtCore.QRect(290, 0, 71, 21))
        self.download_button.setObjectName("download_button")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fresh_button.setText(_translate("MainWindow", "fresh"))
        self.back_button.setText(_translate("MainWindow", "back"))
        self.forward_button.setText(_translate("MainWindow", "forward"))
        self.download_button.setText(_translate("MainWindow", "download"))

