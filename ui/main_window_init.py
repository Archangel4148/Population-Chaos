# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_population_main_window(object):
    def setupUi(self, population_main_window):
        population_main_window.setObjectName("population_main_window")
        population_main_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(population_main_window)
        self.centralwidget.setObjectName("centralwidget")
        population_main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(population_main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        population_main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(population_main_window)
        self.statusbar.setObjectName("statusbar")
        population_main_window.setStatusBar(self.statusbar)

        self.retranslateUi(population_main_window)
        QtCore.QMetaObject.connectSlotsByName(population_main_window)

    def retranslateUi(self, population_main_window):
        _translate = QtCore.QCoreApplication.translate
        population_main_window.setWindowTitle(_translate("population_main_window", "MainWindow"))