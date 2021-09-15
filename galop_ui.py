# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'galop.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1448, 725)
        MainWindow.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid gray;\n"
"    margin-top: 0.5em;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 280, 1131, 391))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.add_current_position = QPushButton(self.tab)
        self.add_current_position.setObjectName(u"add_current_position")
        self.add_current_position.setGeometry(QRect(10, 20, 141, 22))
        self.min_extrusion = QLineEdit(self.tab)
        self.min_extrusion.setObjectName(u"min_extrusion")
        self.min_extrusion.setGeometry(QRect(40, 240, 81, 22))
        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(0, 240, 57, 14))
        self.points_3d = QListWidget(self.tab)
        self.points_3d.setObjectName(u"points_3d")
        self.points_3d.setGeometry(QRect(10, 60, 256, 161))
        self.delete_position = QPushButton(self.tab)
        self.delete_position.setObjectName(u"delete_position")
        self.delete_position.setGeometry(QRect(170, 20, 80, 22))
        self.label_12 = QLabel(self.tab)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(140, 240, 57, 14))
        self.max_extrusion = QLineEdit(self.tab)
        self.max_extrusion.setObjectName(u"max_extrusion")
        self.max_extrusion.setGeometry(QRect(200, 240, 71, 22))
        self.create_volume = QPushButton(self.tab)
        self.create_volume.setObjectName(u"create_volume")
        self.create_volume.setGeometry(QRect(339, 130, 111, 22))
        self.volume_choice = QComboBox(self.tab)
        self.volume_choice.setObjectName(u"volume_choice")
        self.volume_choice.setGeometry(QRect(570, 50, 79, 22))
        self.label_13 = QLabel(self.tab)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(490, 100, 71, 16))
        self.path = QComboBox(self.tab)
        self.path.setObjectName(u"path")
        self.path.setGeometry(QRect(570, 100, 79, 22))
        self.scan_x_step = QLineEdit(self.tab)
        self.scan_x_step.setObjectName(u"scan_x_step")
        self.scan_x_step.setGeometry(QRect(570, 130, 113, 22))
        self.scan_y_step = QLineEdit(self.tab)
        self.scan_y_step.setObjectName(u"scan_y_step")
        self.scan_y_step.setGeometry(QRect(570, 170, 113, 22))
        self.scan_z_step = QLineEdit(self.tab)
        self.scan_z_step.setObjectName(u"scan_z_step")
        self.scan_z_step.setGeometry(QRect(570, 210, 113, 22))
        self.label_14 = QLabel(self.tab)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(500, 130, 57, 14))
        self.label_15 = QLabel(self.tab)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(490, 170, 57, 14))
        self.label_16 = QLabel(self.tab)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(490, 220, 57, 14))
        self.label_17 = QLabel(self.tab)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(490, 50, 57, 14))
        self.create_path = QPushButton(self.tab)
        self.create_path.setObjectName(u"create_path")
        self.create_path.setGeometry(QRect(790, 130, 80, 22))
        self.label_18 = QLabel(self.tab)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(920, 130, 57, 14))
        self.path_choice = QComboBox(self.tab)
        self.path_choice.setObjectName(u"path_choice")
        self.path_choice.setGeometry(QRect(970, 130, 79, 22))
        self.start_scan = QPushButton(self.tab)
        self.start_scan.setObjectName(u"start_scan")
        self.start_scan.setGeometry(QRect(970, 220, 80, 22))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 40, 821, 231))
        self.groupBox.setStyleSheet(u"")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.z_step = QLineEdit(self.groupBox)
        self.z_step.setObjectName(u"z_step")
        self.z_step.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.z_step, 3, 5, 1, 1)

        self.x_acc = QLineEdit(self.groupBox)
        self.x_acc.setObjectName(u"x_acc")
        self.x_acc.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.x_acc, 1, 7, 1, 1)

        self.y_local = QLineEdit(self.groupBox)
        self.y_local.setObjectName(u"y_local")
        self.y_local.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.y_local, 2, 2, 1, 1)

        self.y_global = QLineEdit(self.groupBox)
        self.y_global.setObjectName(u"y_global")
        self.y_global.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.y_global, 2, 1, 1, 1)

        self.home = QPushButton(self.groupBox)
        self.home.setObjectName(u"home")

        self.gridLayout.addWidget(self.home, 5, 6, 1, 2)

        self.y_p = QPushButton(self.groupBox)
        self.y_p.setObjectName(u"y_p")
        self.y_p.setMaximumSize(QSize(40, 16777215))

        self.gridLayout.addWidget(self.y_p, 2, 6, 1, 1)

        self.x_p = QPushButton(self.groupBox)
        self.x_p.setObjectName(u"x_p")
        self.x_p.setMaximumSize(QSize(40, 16777215))

        self.gridLayout.addWidget(self.x_p, 1, 6, 1, 1)

        self.y_m = QPushButton(self.groupBox)
        self.y_m.setObjectName(u"y_m")
        self.y_m.setMaximumSize(QSize(40, 16777215))

        self.gridLayout.addWidget(self.y_m, 2, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 9, 1, 1)

        self.y_acc = QLineEdit(self.groupBox)
        self.y_acc.setObjectName(u"y_acc")
        self.y_acc.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.y_acc, 2, 7, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.z_m = QPushButton(self.groupBox)
        self.z_m.setObjectName(u"z_m")
        self.z_m.setMaximumSize(QSize(40, 16777215))

        self.gridLayout.addWidget(self.z_m, 3, 4, 1, 1)

        self.y_step = QLineEdit(self.groupBox)
        self.y_step.setObjectName(u"y_step")
        self.y_step.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.y_step, 2, 5, 1, 1)

        self.z_acc = QLineEdit(self.groupBox)
        self.z_acc.setObjectName(u"z_acc")
        self.z_acc.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.z_acc, 3, 7, 1, 1)

        self.y_origin = QLineEdit(self.groupBox)
        self.y_origin.setObjectName(u"y_origin")
        self.y_origin.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.y_origin, 2, 3, 1, 1)

        self.x_step = QLineEdit(self.groupBox)
        self.x_step.setObjectName(u"x_step")
        self.x_step.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.x_step, 1, 5, 1, 1)

        self.z_origin = QLineEdit(self.groupBox)
        self.z_origin.setObjectName(u"z_origin")
        self.z_origin.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.z_origin, 3, 3, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(30, 16777215))

        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)

        self.x_speed = QLineEdit(self.groupBox)
        self.x_speed.setObjectName(u"x_speed")
        self.x_speed.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.x_speed, 1, 8, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(30, 16777215))

        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 3, 1, 1)

        self.x_m = QPushButton(self.groupBox)
        self.x_m.setObjectName(u"x_m")
        self.x_m.setMaximumSize(QSize(40, 16777215))

        self.gridLayout.addWidget(self.x_m, 1, 4, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.label_6, 0, 7, 1, 1)

        self.goto_origin = QPushButton(self.groupBox)
        self.goto_origin.setObjectName(u"goto_origin")

        self.gridLayout.addWidget(self.goto_origin, 5, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 5, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)

        self.label_19 = QLabel(self.groupBox)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.label_19, 0, 3, 1, 1)

        self.x_global = QLineEdit(self.groupBox)
        self.x_global.setObjectName(u"x_global")
        self.x_global.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.x_global, 1, 1, 1, 1)

        self.set_origin = QPushButton(self.groupBox)
        self.set_origin.setObjectName(u"set_origin")

        self.gridLayout.addWidget(self.set_origin, 5, 1, 1, 1)

        self.x_origin = QLineEdit(self.groupBox)
        self.x_origin.setObjectName(u"x_origin")
        self.x_origin.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.x_origin, 1, 3, 1, 1)

        self.z_local = QLineEdit(self.groupBox)
        self.z_local.setObjectName(u"z_local")
        self.z_local.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.z_local, 3, 2, 1, 1)

        self.x_local = QLineEdit(self.groupBox)
        self.x_local.setObjectName(u"x_local")
        self.x_local.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.x_local, 1, 2, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.label_7, 0, 8, 1, 1)

        self.z_global = QLineEdit(self.groupBox)
        self.z_global.setObjectName(u"z_global")
        self.z_global.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.z_global, 3, 1, 1, 1)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(30, 16777215))

        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)

        self.z_speed = QLineEdit(self.groupBox)
        self.z_speed.setObjectName(u"z_speed")
        self.z_speed.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.z_speed, 3, 8, 1, 1)

        self.z_p = QPushButton(self.groupBox)
        self.z_p.setObjectName(u"z_p")
        self.z_p.setMaximumSize(QSize(40, 16777215))

        self.gridLayout.addWidget(self.z_p, 3, 6, 1, 1)

        self.y_speed = QLineEdit(self.groupBox)
        self.y_speed.setObjectName(u"y_speed")
        self.y_speed.setMaximumSize(QSize(90, 16777215))

        self.gridLayout.addWidget(self.y_speed, 2, 8, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1448, 19))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.add_current_position.setText(QCoreApplication.translate("MainWindow", u"Add Current position", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Min.", None))
        self.delete_position.setText(QCoreApplication.translate("MainWindow", u"Delete ", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Max", None))
        self.create_volume.setText(QCoreApplication.translate("MainWindow", u"Create Volume ", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Path order", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"step x", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"step y", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"step z", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Volume", None))
        self.create_path.setText(QCoreApplication.translate("MainWindow", u"Create Path", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Path", None))
        self.start_scan.setText(QCoreApplication.translate("MainWindow", u"Start scan", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"3D scan", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"1D Scan", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Movement", None))
        self.home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.y_p.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.x_p.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.y_m.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Global (mm)", None))
        self.z_m.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.x_m.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Acc (mms<sup>-2</sup>)", None))
        self.goto_origin.setText(QCoreApplication.translate("MainWindow", u"Goto Origin", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Step (mm)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Local (mm)", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Origin (mm)", None))
        self.set_origin.setText(QCoreApplication.translate("MainWindow", u"Set Origin", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Speed (mm/s)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.z_p.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Axis", None))
    # retranslateUi

