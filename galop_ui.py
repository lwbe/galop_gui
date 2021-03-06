# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/galop.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1265, 713)
        MainWindow.setStyleSheet("QGroupBox {\n"
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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMaximumSize(QtCore.QSize(731, 231))
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.z_step = QtWidgets.QLineEdit(self.groupBox)
        self.z_step.setMaximumSize(QtCore.QSize(90, 16777215))
        self.z_step.setObjectName("z_step")
        self.gridLayout.addWidget(self.z_step, 3, 5, 1, 1)
        self.x_acc = QtWidgets.QLineEdit(self.groupBox)
        self.x_acc.setMaximumSize(QtCore.QSize(90, 16777215))
        self.x_acc.setObjectName("x_acc")
        self.gridLayout.addWidget(self.x_acc, 1, 7, 1, 1)
        self.y_local = QtWidgets.QLineEdit(self.groupBox)
        self.y_local.setMaximumSize(QtCore.QSize(90, 16777215))
        self.y_local.setObjectName("y_local")
        self.gridLayout.addWidget(self.y_local, 2, 2, 1, 1)
        self.y_global = QtWidgets.QLineEdit(self.groupBox)
        self.y_global.setMaximumSize(QtCore.QSize(90, 16777215))
        self.y_global.setObjectName("y_global")
        self.gridLayout.addWidget(self.y_global, 2, 1, 1, 1)
        self.home = QtWidgets.QPushButton(self.groupBox)
        self.home.setObjectName("home")
        self.gridLayout.addWidget(self.home, 5, 6, 1, 2)
        self.y_p = QtWidgets.QPushButton(self.groupBox)
        self.y_p.setMaximumSize(QtCore.QSize(40, 16777215))
        self.y_p.setObjectName("y_p")
        self.gridLayout.addWidget(self.y_p, 2, 6, 1, 1)
        self.x_p = QtWidgets.QPushButton(self.groupBox)
        self.x_p.setMaximumSize(QtCore.QSize(40, 16777215))
        self.x_p.setObjectName("x_p")
        self.gridLayout.addWidget(self.x_p, 1, 6, 1, 1)
        self.y_m = QtWidgets.QPushButton(self.groupBox)
        self.y_m.setMaximumSize(QtCore.QSize(40, 16777215))
        self.y_m.setObjectName("y_m")
        self.gridLayout.addWidget(self.y_m, 2, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 9, 1, 1)
        self.y_acc = QtWidgets.QLineEdit(self.groupBox)
        self.y_acc.setMaximumSize(QtCore.QSize(90, 16777215))
        self.y_acc.setObjectName("y_acc")
        self.gridLayout.addWidget(self.y_acc, 2, 7, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.z_m = QtWidgets.QPushButton(self.groupBox)
        self.z_m.setMaximumSize(QtCore.QSize(40, 16777215))
        self.z_m.setObjectName("z_m")
        self.gridLayout.addWidget(self.z_m, 3, 4, 1, 1)
        self.y_step = QtWidgets.QLineEdit(self.groupBox)
        self.y_step.setMaximumSize(QtCore.QSize(90, 16777215))
        self.y_step.setObjectName("y_step")
        self.gridLayout.addWidget(self.y_step, 2, 5, 1, 1)
        self.z_acc = QtWidgets.QLineEdit(self.groupBox)
        self.z_acc.setMaximumSize(QtCore.QSize(90, 16777215))
        self.z_acc.setObjectName("z_acc")
        self.gridLayout.addWidget(self.z_acc, 3, 7, 1, 1)
        self.y_origin = QtWidgets.QLineEdit(self.groupBox)
        self.y_origin.setMaximumSize(QtCore.QSize(90, 16777215))
        self.y_origin.setObjectName("y_origin")
        self.gridLayout.addWidget(self.y_origin, 2, 3, 1, 1)
        self.x_step = QtWidgets.QLineEdit(self.groupBox)
        self.x_step.setMaximumSize(QtCore.QSize(90, 16777215))
        self.x_step.setObjectName("x_step")
        self.gridLayout.addWidget(self.x_step, 1, 5, 1, 1)
        self.z_origin = QtWidgets.QLineEdit(self.groupBox)
        self.z_origin.setMaximumSize(QtCore.QSize(90, 16777215))
        self.z_origin.setObjectName("z_origin")
        self.gridLayout.addWidget(self.z_origin, 3, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.x_speed = QtWidgets.QLineEdit(self.groupBox)
        self.x_speed.setMaximumSize(QtCore.QSize(90, 16777215))
        self.x_speed.setObjectName("x_speed")
        self.gridLayout.addWidget(self.x_speed, 1, 8, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 3, 1, 1)
        self.x_m = QtWidgets.QPushButton(self.groupBox)
        self.x_m.setMaximumSize(QtCore.QSize(40, 16777215))
        self.x_m.setObjectName("x_m")
        self.gridLayout.addWidget(self.x_m, 1, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 7, 1, 1)
        self.goto_origin = QtWidgets.QPushButton(self.groupBox)
        self.goto_origin.setObjectName("goto_origin")
        self.gridLayout.addWidget(self.goto_origin, 5, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 5, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.groupBox)
        self.label_19.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 0, 3, 1, 1)
        self.x_global = QtWidgets.QLineEdit(self.groupBox)
        self.x_global.setMaximumSize(QtCore.QSize(90, 16777215))
        self.x_global.setObjectName("x_global")
        self.gridLayout.addWidget(self.x_global, 1, 1, 1, 1)
        self.set_origin = QtWidgets.QPushButton(self.groupBox)
        self.set_origin.setObjectName("set_origin")
        self.gridLayout.addWidget(self.set_origin, 5, 1, 1, 1)
        self.x_origin = QtWidgets.QLineEdit(self.groupBox)
        self.x_origin.setMaximumSize(QtCore.QSize(90, 16777215))
        self.x_origin.setObjectName("x_origin")
        self.gridLayout.addWidget(self.x_origin, 1, 3, 1, 1)
        self.z_local = QtWidgets.QLineEdit(self.groupBox)
        self.z_local.setMaximumSize(QtCore.QSize(90, 16777215))
        self.z_local.setObjectName("z_local")
        self.gridLayout.addWidget(self.z_local, 3, 2, 1, 1)
        self.x_local = QtWidgets.QLineEdit(self.groupBox)
        self.x_local.setMaximumSize(QtCore.QSize(90, 16777215))
        self.x_local.setObjectName("x_local")
        self.gridLayout.addWidget(self.x_local, 1, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 8, 1, 1)
        self.z_global = QtWidgets.QLineEdit(self.groupBox)
        self.z_global.setMaximumSize(QtCore.QSize(90, 16777215))
        self.z_global.setObjectName("z_global")
        self.gridLayout.addWidget(self.z_global, 3, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)
        self.z_speed = QtWidgets.QLineEdit(self.groupBox)
        self.z_speed.setMaximumSize(QtCore.QSize(90, 16777215))
        self.z_speed.setObjectName("z_speed")
        self.gridLayout.addWidget(self.z_speed, 3, 8, 1, 1)
        self.z_p = QtWidgets.QPushButton(self.groupBox)
        self.z_p.setMaximumSize(QtCore.QSize(40, 16777215))
        self.z_p.setObjectName("z_p")
        self.gridLayout.addWidget(self.z_p, 3, 6, 1, 1)
        self.y_speed = QtWidgets.QLineEdit(self.groupBox)
        self.y_speed.setMaximumSize(QtCore.QSize(90, 16777215))
        self.y_speed.setObjectName("y_speed")
        self.gridLayout.addWidget(self.y_speed, 2, 8, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setMaximumSize(QtCore.QSize(300, 231))
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_20 = QtWidgets.QLabel(self.groupBox_3)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 0, 0, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.groupBox_3)
        self.label_24.setObjectName("label_24")
        self.gridLayout_3.addWidget(self.label_24, 0, 1, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.groupBox_3)
        self.label_30.setObjectName("label_30")
        self.gridLayout_3.addWidget(self.label_30, 0, 2, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.groupBox_3)
        self.label_21.setObjectName("label_21")
        self.gridLayout_3.addWidget(self.label_21, 1, 0, 1, 1)
        self.field_x = QtWidgets.QLabel(self.groupBox_3)
        self.field_x.setObjectName("field_x")
        self.gridLayout_3.addWidget(self.field_x, 1, 1, 1, 1)
        self.field_range_x = QtWidgets.QComboBox(self.groupBox_3)
        self.field_range_x.setObjectName("field_range_x")
        self.gridLayout_3.addWidget(self.field_range_x, 1, 2, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.groupBox_3)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 2, 0, 1, 1)
        self.field_y = QtWidgets.QLabel(self.groupBox_3)
        self.field_y.setObjectName("field_y")
        self.gridLayout_3.addWidget(self.field_y, 2, 1, 1, 1)
        self.field_range_y = QtWidgets.QComboBox(self.groupBox_3)
        self.field_range_y.setObjectName("field_range_y")
        self.gridLayout_3.addWidget(self.field_range_y, 2, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 2, 3, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.groupBox_3)
        self.label_23.setObjectName("label_23")
        self.gridLayout_3.addWidget(self.label_23, 3, 0, 1, 1)
        self.field_z = QtWidgets.QLabel(self.groupBox_3)
        self.field_z.setObjectName("field_z")
        self.gridLayout_3.addWidget(self.field_z, 3, 1, 1, 1)
        self.field_range_z = QtWidgets.QComboBox(self.groupBox_3)
        self.field_range_z.setObjectName("field_range_z")
        self.gridLayout_3.addWidget(self.field_range_z, 3, 2, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.groupBox_3)
        self.label_28.setObjectName("label_28")
        self.gridLayout_3.addWidget(self.label_28, 4, 0, 1, 1)
        self.field_norm = QtWidgets.QLabel(self.groupBox_3)
        self.field_norm.setObjectName("field_norm")
        self.gridLayout_3.addWidget(self.field_norm, 4, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 5, 2, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox_3, 0, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.add_current_position = QtWidgets.QPushButton(self.groupBox_6)
        self.add_current_position.setObjectName("add_current_position")
        self.gridLayout_12.addWidget(self.add_current_position, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(18, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_12.addItem(spacerItem4, 0, 1, 1, 1)
        self.delete_position = QtWidgets.QPushButton(self.groupBox_6)
        self.delete_position.setObjectName("delete_position")
        self.gridLayout_12.addWidget(self.delete_position, 0, 2, 1, 1)
        self.points_3d = QtWidgets.QListWidget(self.groupBox_6)
        self.points_3d.setObjectName("points_3d")
        self.gridLayout_12.addWidget(self.points_3d, 1, 0, 1, 3)
        self.gridLayout_13.addLayout(self.gridLayout_12, 0, 0, 1, 1)
        self.gridLayout_14.addWidget(self.groupBox_6, 0, 0, 1, 1)
        self.create_volume = QtWidgets.QPushButton(self.tab)
        self.create_volume.setObjectName("create_volume")
        self.gridLayout_14.addWidget(self.create_volume, 0, 1, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.delete_volume = QtWidgets.QPushButton(self.groupBox_4)
        self.delete_volume.setObjectName("delete_volume")
        self.gridLayout_4.addWidget(self.delete_volume, 0, 0, 1, 2)
        self.label_17 = QtWidgets.QLabel(self.groupBox_4)
        self.label_17.setObjectName("label_17")
        self.gridLayout_4.addWidget(self.label_17, 1, 0, 1, 1)
        self.volume_choice = QtWidgets.QComboBox(self.groupBox_4)
        self.volume_choice.setObjectName("volume_choice")
        self.gridLayout_4.addWidget(self.volume_choice, 1, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem5, 2, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox_4)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 3, 0, 1, 1)
        self.path = QtWidgets.QComboBox(self.groupBox_4)
        self.path.setObjectName("path")
        self.gridLayout_4.addWidget(self.path, 3, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox_4)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 4, 0, 1, 1)
        self.scan_x_step = QtWidgets.QLineEdit(self.groupBox_4)
        self.scan_x_step.setObjectName("scan_x_step")
        self.gridLayout_4.addWidget(self.scan_x_step, 4, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox_4)
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 5, 0, 1, 1)
        self.scan_y_step = QtWidgets.QLineEdit(self.groupBox_4)
        self.scan_y_step.setObjectName("scan_y_step")
        self.gridLayout_4.addWidget(self.scan_y_step, 5, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.groupBox_4)
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 6, 0, 1, 1)
        self.scan_z_step = QtWidgets.QLineEdit(self.groupBox_4)
        self.scan_z_step.setObjectName("scan_z_step")
        self.gridLayout_4.addWidget(self.scan_z_step, 6, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.groupBox_4)
        self.label_25.setObjectName("label_25")
        self.gridLayout_4.addWidget(self.label_25, 7, 0, 1, 1)
        self.pathtype_choice = QtWidgets.QComboBox(self.groupBox_4)
        self.pathtype_choice.setObjectName("pathtype_choice")
        self.gridLayout_4.addWidget(self.pathtype_choice, 7, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.groupBox_4)
        self.label_26.setObjectName("label_26")
        self.gridLayout_4.addWidget(self.label_26, 8, 0, 1, 1)
        self.direction_choice = QtWidgets.QComboBox(self.groupBox_4)
        self.direction_choice.setObjectName("direction_choice")
        self.gridLayout_4.addWidget(self.direction_choice, 8, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.gridLayout_14.addWidget(self.groupBox_4, 0, 2, 2, 1)
        self.create_path = QtWidgets.QPushButton(self.tab)
        self.create_path.setObjectName("create_path")
        self.gridLayout_14.addWidget(self.create_path, 0, 3, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.delete_path = QtWidgets.QPushButton(self.groupBox_5)
        self.delete_path.setObjectName("delete_path")
        self.gridLayout_6.addWidget(self.delete_path, 0, 0, 1, 2)
        self.label_18 = QtWidgets.QLabel(self.groupBox_5)
        self.label_18.setObjectName("label_18")
        self.gridLayout_6.addWidget(self.label_18, 1, 0, 1, 1)
        self.path_choice = QtWidgets.QComboBox(self.groupBox_5)
        self.path_choice.setMinimumSize(QtCore.QSize(150, 0))
        self.path_choice.setObjectName("path_choice")
        self.gridLayout_6.addWidget(self.path_choice, 1, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem6, 2, 1, 1, 1)
        self.save_scan = QtWidgets.QPushButton(self.groupBox_5)
        self.save_scan.setObjectName("save_scan")
        self.gridLayout_6.addWidget(self.save_scan, 3, 0, 1, 2)
        self.start_scan = QtWidgets.QPushButton(self.groupBox_5)
        self.start_scan.setObjectName("start_scan")
        self.gridLayout_6.addWidget(self.start_scan, 4, 0, 1, 2)
        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.gridLayout_14.addWidget(self.groupBox_5, 0, 4, 2, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_10.addWidget(self.label, 0, 0, 1, 1)
        self.extrusion_axis = QtWidgets.QComboBox(self.groupBox_2)
        self.extrusion_axis.setMaximumSize(QtCore.QSize(75, 16777215))
        self.extrusion_axis.setObjectName("extrusion_axis")
        self.gridLayout_10.addWidget(self.extrusion_axis, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_10.addWidget(self.label_9, 1, 0, 1, 1)
        self.min_extrusion = QtWidgets.QLineEdit(self.groupBox_2)
        self.min_extrusion.setMaximumSize(QtCore.QSize(75, 16777215))
        self.min_extrusion.setObjectName("min_extrusion")
        self.gridLayout_10.addWidget(self.min_extrusion, 1, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setObjectName("label_12")
        self.gridLayout_10.addWidget(self.label_12, 1, 2, 1, 1)
        self.max_extrusion = QtWidgets.QLineEdit(self.groupBox_2)
        self.max_extrusion.setMaximumSize(QtCore.QSize(75, 16777215))
        self.max_extrusion.setObjectName("max_extrusion")
        self.gridLayout_10.addWidget(self.max_extrusion, 1, 3, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_10, 0, 0, 1, 1)
        self.gridLayout_14.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.gridLayout_15.addLayout(self.gridLayout_14, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_9.addWidget(self.tabWidget, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1265, 19))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuDebug = QtWidgets.QMenu(self.menubar)
        self.menuDebug.setObjectName("menuDebug")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_scan_param = QtWidgets.QAction(MainWindow)
        self.actionLoad_scan_param.setObjectName("actionLoad_scan_param")
        self.actionSave_scan_param = QtWidgets.QAction(MainWindow)
        self.actionSave_scan_param.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionSave_scan_param.setObjectName("actionSave_scan_param")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionGet_Position = QtWidgets.QAction(MainWindow)
        self.actionGet_Position.setObjectName("actionGet_Position")
        self.actionGet_Field = QtWidgets.QAction(MainWindow)
        self.actionGet_Field.setObjectName("actionGet_Field")
        self.menuFile.addAction(self.actionLoad_scan_param)
        self.menuFile.addAction(self.actionSave_scan_param)
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuDebug.addAction(self.actionGet_Position)
        self.menuDebug.addAction(self.actionGet_Field)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDebug.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "galop_bench"))
        self.groupBox.setTitle(_translate("MainWindow", "Movement"))
        self.home.setText(_translate("MainWindow", "Home"))
        self.y_p.setText(_translate("MainWindow", "+"))
        self.x_p.setText(_translate("MainWindow", "+"))
        self.y_m.setText(_translate("MainWindow", "-"))
        self.label_3.setText(_translate("MainWindow", "Global (mm)"))
        self.z_m.setText(_translate("MainWindow", "-"))
        self.label_8.setText(_translate("MainWindow", "X"))
        self.label_10.setText(_translate("MainWindow", "Y"))
        self.x_m.setText(_translate("MainWindow", "-"))
        self.label_6.setText(_translate("MainWindow", "Acc (mms<sup>-2</sup>)"))
        self.goto_origin.setText(_translate("MainWindow", "Goto Origin"))
        self.label_5.setText(_translate("MainWindow", "Step (mm)"))
        self.label_4.setText(_translate("MainWindow", "Local (mm)"))
        self.label_19.setText(_translate("MainWindow", "Origin (mm)"))
        self.set_origin.setText(_translate("MainWindow", "Set Origin"))
        self.label_7.setText(_translate("MainWindow", "Speed (mm/s)"))
        self.label_11.setText(_translate("MainWindow", "Z"))
        self.z_p.setText(_translate("MainWindow", "+"))
        self.label_2.setText(_translate("MainWindow", "Axis"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Gaussmeter"))
        self.label_20.setText(_translate("MainWindow", "Component"))
        self.label_24.setText(_translate("MainWindow", "Value"))
        self.label_30.setText(_translate("MainWindow", "Range"))
        self.label_21.setText(_translate("MainWindow", "X"))
        self.field_x.setText(_translate("MainWindow", "0.0"))
        self.label_22.setText(_translate("MainWindow", "Y"))
        self.field_y.setText(_translate("MainWindow", "0.0"))
        self.label_23.setText(_translate("MainWindow", "Z"))
        self.field_z.setText(_translate("MainWindow", "0.0"))
        self.label_28.setText(_translate("MainWindow", "Norm"))
        self.field_norm.setText(_translate("MainWindow", "0.0"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Points"))
        self.add_current_position.setText(_translate("MainWindow", "Add Current position"))
        self.delete_position.setText(_translate("MainWindow", "Delete "))
        self.create_volume.setText(_translate("MainWindow", "Create Volume "))
        self.groupBox_4.setTitle(_translate("MainWindow", "Volume definition"))
        self.delete_volume.setText(_translate("MainWindow", "Delete Volume"))
        self.label_17.setText(_translate("MainWindow", "Volume"))
        self.label_13.setText(_translate("MainWindow", "Path order"))
        self.label_14.setText(_translate("MainWindow", "step x"))
        self.label_15.setText(_translate("MainWindow", "step y"))
        self.label_16.setText(_translate("MainWindow", "step z"))
        self.label_25.setText(_translate("MainWindow", "Path type"))
        self.label_26.setText(_translate("MainWindow", "Directions"))
        self.create_path.setText(_translate("MainWindow", "Create Path"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Path definition"))
        self.delete_path.setText(_translate("MainWindow", "Delete Path"))
        self.label_18.setText(_translate("MainWindow", "Path"))
        self.save_scan.setText(_translate("MainWindow", "Save scan"))
        self.start_scan.setText(_translate("MainWindow", "Start scan"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Extrusion"))
        self.label.setText(_translate("MainWindow", "Axis"))
        self.label_9.setText(_translate("MainWindow", "Min."))
        self.label_12.setText(_translate("MainWindow", "Max"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "3D scan"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "1D Scan"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuDebug.setTitle(_translate("MainWindow", "Debug"))
        self.actionLoad_scan_param.setText(_translate("MainWindow", "Load scan param"))
        self.actionLoad_scan_param.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave_scan_param.setText(_translate("MainWindow", "Save scan param"))
        self.actionSave_scan_param.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionGet_Position.setText(_translate("MainWindow", "Get Position"))
        self.actionGet_Field.setText(_translate("MainWindow", "Get Field"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
