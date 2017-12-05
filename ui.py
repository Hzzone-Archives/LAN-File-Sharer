# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import utils
import transfer
import config
import json
import time

class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.host_listview = QtWidgets.QListView(self.centralWidget)
        self.host_listview.setGeometry(QtCore.QRect(0, 0, 151, 301))
        self.host_listview.setObjectName("host_listview")
        self.host_listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.file_listview = QtWidgets.QTreeView(self.centralWidget)
        self.file_listview.setGeometry(QtCore.QRect(150, 20, 251, 281))
        self.file_listview.setObjectName("file_listview")
        self.file_listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
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

        self.file_model = QStandardItemModel(self.file_listview)
        self.host_model = QStandardItemModel(self.file_listview)

        self.init_host()
        # self.init_file_list()

        self.file_listview.expanded.connect(self.init_file_list)
        self.host_listview.doubleClicked.connect(self.init_file_list)

        self.file_listview.setModel(self.file_model)
        self.host_listview.setModel(self.host_model)

        self.file_model.setHorizontalHeaderLabels(["路径"])
        # self.file_model.setHorizontalHeaderLabels(["路径", "文件大小"])

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fresh_button.setText(_translate("MainWindow", "fresh"))
        self.back_button.setText(_translate("MainWindow", "back"))
        self.forward_button.setText(_translate("MainWindow", "forward"))
        self.download_button.setText(_translate("MainWindow", "download"))

    def init_host(self):
        self.host_model.clear()
        effective_ip = utils.scan_lan()
        for each_ip in effective_ip:
            self.host_model.appendRow(QStandardItem(each_ip))

    def init_file_list(self, signal):
        my_sender = self.sender()
        if isinstance(my_sender, QListView):
            self.file_model.clear()
            self.file_model.setHorizontalHeaderLabels(["路径"])
            transfer_thread = transfer.Client_transfer((utils.get_internal_ip(), config.server_port), "*")
            transfer_thread.start()
            # time.sleep(config.sleep_time)
            while not transfer_thread.recvd_content:
                pass
            data = json.loads(transfer_thread.recvd_content)
            for key, value in sorted(data.items(), key=lambda d: d[1], reverse=True):
                if not value:
                    self.file_model.appendRow(QStandardItem(key))
                else:
                    i = QStandardItem(key)
                    i.appendRow(QStandardItem(""))
                    self.file_model.appendRow(i)
        else:
            item = self.file_model.itemFromIndex(signal)
            item.removeRows(0, item.rowCount())
            parent_item = item.parent()
            path_list = [item.text()]
            while parent_item:
                # path_list.append(parent_item.text())
                path_list.insert(0, parent_item.text())
                parent_item = parent_item.parent()
            print(path_list)
            transfer_thread = transfer.Client_transfer((utils.get_internal_ip(), config.server_port), json.dumps(path_list))
            transfer_thread.start()
            # time.sleep(config.sleep_time)
            while not transfer_thread.recvd_content:
                pass
            data = json.loads(transfer_thread.recvd_content)
            for key, value in sorted(data.items(), key=lambda d: d[1], reverse=True):
                if not value:
                    item.appendRow(QStandardItem(key))
                else:
                    i = QStandardItem(key)
                    i.appendRow(QStandardItem(""))
                    item.appendRow(i)
            # item.appendRow(QStandardItem("hh"))
            # print(data)


    def md(self, signal):
        print(self.file_model.itemFromIndex(signal))


