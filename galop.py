#! coding: utf-8

# Generic imports
import sys
import time
import json
from pprint import pprint
from datetime import datetime

import click
import numpy as np

#PyQt Imports
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QWidget,
    QDialogButtonBox,
    QVBoxLayout, QGridLayout,
    QLabel,
    QMessageBox,
    QFileDialog,
    QLineEdit,
    QComboBox
)
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QDoubleValidator, QValidator

# matplotlib imports
#from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

# Ui imports
from galop_ui import Ui_MainWindow
from scan3dwidget_ui import Ui_Form


import paths

module_to_start = """
cmdmod /opt/pyrame/cmd_serial.xml &
cmdmod /opt/pyrame/cmd_gpib.xml &
cmdmod /opt/pyrame/cmd_th_apt.xml &
cmdmod /opt/pyrame/cmd_motion.xml &
cmdmod /opt/pyrame/cmd_paths.xml &
cmdmod /opt/pyrame/cmd_ls_460.xml &
"""

_Nx, _Xi, _Xf, _Ny, _Yi, _Yf, _Nz, _Zi, _Zf = 10, -2, 2, 10, -2, 2, 10, -2, 2

# datas should be taken from a file
initial_values = {
    "x_origin" : "0.0",
    "x_step": "5.0",
    "x_acc": "2",
    "x_speed": "2",
    "y_origin": "0.0",
    "y_step": "5.0",
    "y_acc": "2",
    "y_speed": "2",
    "z_origin" : "0.0",
    "z_step": "5.0",
    "z_acc": "2",
    "z_speed": "2",
    "min_extrusion": "0",
    "max_extrusion": "1",
    "scan_x_step": "1",
    "scan_y_step": "1",
    "scan_z_step": "1",
}

pyrame_modules_list = [
            "motion",
            "th_apt",
            "bus",
            "serial",
            "gpib",
            "multimeter",
            "ls460",
        ]

pyrame_modules_configuration = {
    "motion": {
        "axis_x": {
            "init": ["th_apt(model=LTS300,bus=serial(serialnum=45839057))"],
            "config": ["300", "0"]
        },
        "axis_y": {
            "init": ["th_apt(model=BSC1_LNR50,bus=serial(serialnum=40828799),chan=1)"],
            "config": ["50", "0"]
        },
        "axis_z": {
            "init": ["th_apt(model=HSLTS300,bus=serial(serialnum=45897070))"],
            "config": ["300", "0"]
        },
    },
    "ls_460": {
        "gaussmeter": {
            "init": [
                "ls_460(bus=gpib(bus=serial(vendor=0403,product=6001,timeout=10),dst_addr=12),Bunits=T,Bmode=0,Bfilter=0,nb_channels=3)"],
            "config": []
        },
    },
}

SIMULATE = None

############################################################################################################
class Pyrame(object):
    def __init__(self,parent):
        self.module_port = {}
        self.parent = parent
        self.simulated_position = [0, 0, 0]
        self.simulated_field = [0, 0, 0, 0]
        self.poly_coords = None
        self.ext_axis = None
        self.ext_limits = None
        self.points = {}
        self.max_points = {}

        # pyrame
        if not SIMULATE:
            import bindpyrame

    # Pyrame Stuff
    def initModules(self,pyrame_modules_configuration):
        # read conf file
        if SIMULATE:
            return
        self.module_port = {}
        self.pyrame_modules_init = pyrame_modules_configuration
        for module, values in self.pyrame_modules_init.items():
            self.module_port[module] = int(bindpyrame.get_port(module.upper()))
            for uid, params in values.items():
                print(module,self.module_port[module],uid,params)
                # we usually have to init first and then config unless it is explicitly different
                order = params.get('init_order', ["init", "config"])
                if order:
                    for function in order:
                        retcode, res = self.call(
                            "%s@%s" % (function,module),
                            uid,
                            *params[function]
                        )

    def deinitModules(self):
        if SIMULATE:
            return
        # we inval and deinit the modules
        for module, values in self.pyrame_modules_init.items():
            for uid, params in values.items():
                order = params.get('deinit_order', ["inval","deinit"])
                for function in order:
                         retcode, res = self.call(
                             "%s@%s" % (function, module),
                             uid
                         )

    def call_simulate(self, pyrame_func, *args):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        print("pyrame call :", pyrame_func, args)
        retval = "ok"
        if pyrame_func.startswith("init@"):
            pass
        elif pyrame_func.startswith("config@"):
            pass
        elif pyrame_func.startswith("get_pos@"):
            if args[0] == "axis_x":
                retval = str(self.simulated_position[0])
            elif args[0] == "axis_y":
                retval = str(self.simulated_position[1])
            else:
                retval = str(self.simulated_position[2])


        elif pyrame_func.startswith("measure@"):
            retval = ",".join([str(i) for i in self.simulated_field])
            print("measure ", retval)
        elif pyrame_func.startswith("move@motion"):
            print("args", args)
            if args[0] == "axis_x":
                self.simulated_position = [self.simulated_position[0] + float(args[1]), self.simulated_position[1], self.simulated_position[2]]
            elif args[0] == "axis_y":
                self.simulated_position = [self.simulated_position[0], self.simulated_position[1] + float(args[1]), self.simulated_position[2]]
            else:
                self.simulated_position = [self.simulated_position[0], self.simulated_position[1], self.simulated_position[2] + float(args[1])]
            # pour simuler des données on calcule la valeur d'une fonction au point d'espace ou on est.
            x, y, z = self.simulated_position
            bx = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
            by = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
            bz = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) * np.sin(np.pi * z))
            bn = np.sqrt(bx*bx + by*by + bz*bz)
            self.simulated_field = [bx,by,bz,bn]
            time.sleep(0.1)
        elif pyrame_func.startswith("move_space@"):
            self.simulated_position = [float(args[1]), float(args[2]), float(args[3])]
        elif pyrame_func.startswith("init_volume"):
            # le prototype de la fonction est
            # "init_volume@paths",\
            #    0       1          2             3              4          5         6         7
            # vol_id, "space_1", math_module, math_function, new_coords, ext_axis, axis_min, axis_max

            # on extrait les points
            self.poly_coords = []
            for i in args[4].split(";")[:-1]:
                self.poly_coords.append([float(j) for j in i.split(",")])
            self.poly_coords = np.array(self.poly_coords)
            self.ext_axis = args[5]
            self.ext_limits = [float(args[6]), float(args[7])]

        elif pyrame_func.startswith("init_path"):
            # le prototype de la fonction est
            # init_path@paths",
            # et les arguments
            #   0         1          2         3          4              5          6          7           8
            # path_id, "space_1", vol_id, scan_x_step, scan_y_step, scan_z_step, path_order, path_type, path_directions

            steps = [float(args[3]), float(args[4]), float(args[5])]
            path_order = args[6]
            path_type = args[7]
            path_directions = args[8]
            path_id = args[0]
            self.points[path_id] = paths.generate_path(self.poly_coords, self.ext_axis, self.ext_limits,
                                                steps, path_order, path_type, path_directions)
            self.max_points[path_id] = self.points[path_id].shape[0]
            retval = "ok"
        elif pyrame_func.startswith("get_path_length"):
            path_id = args[0]
            retval = "%s" % self.max_points[path_id]
        elif pyrame_func.startswith("get_path"):
            path_id = args[0]
            retval = ";".join(["%s,%s,%s" % (p[0], p[1], p[2]) for p in self.points[path_id]])
        elif pyrame_func.startswith("move_first"):
            path_id = args[0]
            print("path_id ", path_id)
            self.current_point = 0
            self.simulated_position = self.points[path_id][self.current_point]
            x, y, z = self.simulated_position
            bx = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
            by = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
            bz = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) * np.sin(np.pi * z))
            bn = np.sqrt(bx*bx + by*by + bz*bz)
            self.simulated_field = [bx,by,bz,bn]
            time.sleep(0.1)

        elif pyrame_func.startswith("move_next"):
            path_id = args[0]

            self.current_point += 1
            print(self.current_point, self.max_points)
            if self.current_point == self.max_points[path_id]:
                retval = "finished"
            else:
                self.simulated_position = self.points[path_id][self.current_point]
                x, y, z = self.simulated_position
                bx = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
                by = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
                bz = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) * np.sin(np.pi * z))
                bn = np.sqrt(bx * bx + by * by + bz * bz)
                self.simulated_field = [bx, by, bz, bn]
                time.sleep(0.5)
        else:
            print("pyrame call : UNKNOWN function", pyrame_func, args)
        QApplication.restoreOverrideCursor()
        return 1, retval

    def call(self, pyrame_func, *args):
        """
        Function to call pyrame module and prevent user action. Inform user in case of error

        :param pyrame_func: the pyrame function to call in the form function@module
        :param args: the args of the function
        :return: the return of the pyrame module
        """
        if SIMULATE:
            return self.call_simulate(pyrame_func, *args)

        QApplication.setOverrideCursor(Qt.WaitCursor)
        function, module = pyrame_func.split("@")
        retcode, res = bindpyrame.sendcmd("localhost",
                                          self.module_port[module],
                                          "%s_%s" % (function, module),
                                          *args)
        if retcode == 0:
            # see stack overflow to customize message box
            # https://stackoverflow.com/questions/37201338/how-to-place-custom-image-onto-qmessagebox
            # messagebox.setIconPixmap(QPixmap(":/images/image_file)) where image_file is the
            messagenbox = QMessageBox.question(
                self.parent,
                "Error calling pyrame",
                "%s" % res,
                buttons=QMessageBox.Ok)

        QApplication.restoreOverrideCursor()
        return retcode, res

###########################################################################
# thread for scan
class Worker(QObject):
    finished = pyqtSignal()
    field = pyqtSignal()

    def __init__(self, path, move_params, pyrame, master_widget):
        super().__init__()
        self._isrunning = True
        self.pyrame = pyrame
        self.move_params = move_params
        self._issuspended = False
        self.master_widget = master_widget
        self.path = path

    def stop(self):
        self._isrunning = False

    def suspend(self):
        self._issuspended = not self._issuspended

    def run(self):

        retcode, res = self.pyrame.call("get_pos@motions", "axis_x")
        x = float(res)
        retcode, res = self.pyrame.call("get_pos@motions", "axis_y")
        y = float(res)
        retcode, res = self.pyrame.call("get_pos@motions", "axis_z")
        z = float(res)
        current_point = np.array([x, y, z])

        speed = self.move_params[0:3]
        acc = self.move_params[3:6]
        run = True
        index = 0
        while run:
            if not self._issuspended:
                p = self.path[index]
                steps = p - current_point
                retcode, res = self.pyrame.call("move@motion","axis_x", str(steps[0]), speed[0], acc[0])
                retcode, res = self.pyrame.call("move@motion","axis_y", str(steps[1]), speed[1], acc[1])
                retcode, res = self.pyrame.call("move@motion","axis_z", str(steps[2]), speed[2], acc[2])

                self.master_widget.updatePositionWidget()
                self.master_widget.updateGaussmeterWidget()
                self.field.emit() #"%s;%s" % (position, field))
                index += 1
                if index == self.path.shape[0] or not self._isrunning:
                    run = False

                current_point = p
        self.finished.emit()

############################################################################################################
# Custom widget
class orderedMovement_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ordered move")

        self.explanation = QLabel('')

        orderLabel = QLabel("&Order")
        self.orderCombo = QComboBox()
        orderLabel.setBuddy(self.orderCombo)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QGridLayout()
        self.layout.addWidget(self.explanation, 0, 0, 1, 2)
        self.layout.addWidget(orderLabel, 1, 0)
        self.layout.addWidget(self.orderCombo, 1, 1)
        self.layout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.setLayout(self.layout)

############################################################################################################
class askForName(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle("Ask for name")

            self.message = QLabel('')
            self.lineEditField = QLineEdit()

            QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
            self.buttonBox = QDialogButtonBox(QBtn)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            self.layout = QVBoxLayout()
            self.layout.addWidget(self.message)
            self.layout.addWidget(self.lineEditField)
            self.layout.addWidget(self.buttonBox)
            self.setLayout(self.layout)

# 3D scan class
#class Scan3dPlotWidget(QWidget, Ui_Form):
#    def __init__(self, parent=None):
#        super(Scan3dPlotWidget,self).__init__(parent)
#        self.setupUi(self)
#        self.stop.clicked.connect(self.close)

############################################################################################################
# 3D scan class
#class Scan3dPlotDialog(QDialog, Ui_Dialog):
class Scan3dPlotDialog(QDialog, Ui_Form):

    def __init__(self, working_thread, parent=None):
        super(Scan3dPlotDialog, self).__init__(parent)
        self.working_thread = working_thread

        # needed for the plot widget
        # and need to add
        # from matplotlib.backends.backend_qt5agg import FigureCanvas
        # and replace
        # self.canvas = QtWidgets.QWidget(Form)
        # by
        #self.canvas = FigureCanvas(self.fig) #QtWidgets.QWidget(Form)
        # in the pyuic file

        self.fig = Figure(figsize=(10, 7.5))
        self.setupUi(self)

        self.scan3d_stop.clicked.connect(self.stop)
        self.scan3d_suspend.clicked.connect(self.suspend)
        self.scan3d_update.setChecked(True)
        self.scan3d_plane.addItems(["xy", "yz", "xz"])
        self.scan3d_fieldcomponent.addItems(["Bx", "By", "Bz", "B norm"])
#        self.scan3d_plottype.addItems(["surface","surface and contour","wireframe"])
        self.scan3d_plottype.addItems(["surface", "wireframe", "contour", "quiver"])

        self.scan3d_plottype.currentTextChanged.connect(self.update_plot_type)
        self.scan3d_plane.currentTextChanged.connect(self.update_layers)
        self.scan3d_layer.currentTextChanged.connect(self.update_plot_params)
        self.scan3d_layer_slider.valueChanged.connect(self.update_plot_params_slider)

        self.scan3d_fieldcomponent.currentTextChanged.connect(self.update_field)

        self._ax = self.canvas.figure.add_subplot(projection="3d")
        self._ax.view_init(30, 30)
        self.plot_object = None
        self.quiver_mode = False

    def stop(self):
        # on demande confirmation pour fermer le fenêtre si on a pas fini l'acquisition.
        if self.scan3d_stop.text != "Close":
            button = QMessageBox.question(self,
                                          "Quit",
                                          "Are you sure you want to stop ?",
                                          buttons=QMessageBox.Yes | QMessageBox.No,
                                          defaultButton=QMessageBox.Yes,
                                          )
            if button == QMessageBox.No:
                return None
        self.working_thread.stop()
        self.accept()

    def suspend(self):
        self.working_thread.suspend()
        if self.scan3d_suspend.text() == "Suspend":
            self.scan3d_suspend.setText("Resume")
        else:
            self.scan3d_suspend.setText("Suspend")

    def init_plot_data(self, data_structure):
        nx, xi, xf, ny, yi, yf, nz, zi, zf = data_structure
        self.Field = np.zeros([nx, ny, nz, 4])
        self.X = np.linspace(xi, xf, nx)
        self.Y = np.linspace(yi, yf, ny)
        self.Z = np.linspace(zi, zf, nz)
        self.all_elements = nx*ny*nz
        self.update_field()
        self.update_layers()
        # should not be needed
        self.update_plot_params()

    def update_field(self):
        self._ax.set_zlabel(self.scan3d_fieldcomponent.currentText())
        self.update_plot_params()

    def update_layers(self):
        plane = self.scan3d_plane.currentText()
        self.scan3d_layer.clear()
        if plane == "xy":
            self.scan3d_layer.addItems([str(i) for i in self.Z])
            self.scan3d_layer_slider.setMinimum(0)
            self.scan3d_layer_slider.setMaximum(len(self.Z)-1)
            self._ax.set_xlabel("Y")
            self._ax.set_ylabel("X")
        elif plane == "yz":
            self.scan3d_layer.addItems([str(i) for i in self.X])
            self.scan3d_layer_slider.setMinimum(0)
            self.scan3d_layer_slider.setMaximum(len(self.X)-1)
            self._ax.set_xlabel("Z")
            self._ax.set_ylabel("Y")
        elif plane == "xz":
            self.scan3d_layer.addItems([str(i) for i in self.Y])
            self.scan3d_layer_slider.setMinimum(0)
            self.scan3d_layer_slider.setMaximum(len(self.Y)-1)
            self._ax.set_xlabel("Z")
            self._ax.set_ylabel("X")
        self.update_plot_params()

    def update_plot_params_slider(self):
        index = self.scan3d_layer_slider.value()
        self.scan3d_layer.setCurrentIndex(index)
        self.update_plot_params()

    def update_plot_params(self):
        plane = self.scan3d_plane.currentText()
        index_layer = self.scan3d_layer.currentIndex()
        self.scan3d_layer_slider.setValue(index_layer)

        field_component_index = self.scan3d_fieldcomponent.currentIndex()
        if plane == "xy":
            self.X_plot, self.Y_plot = np.meshgrid(self.Y, self.X)
            self.Z_plot = self.Field[:, :, index_layer, field_component_index]
        elif plane == "yz":
            self.X_plot, self.Y_plot = np.meshgrid(self.Z, self.Y)
            self.Z_plot = self.Field[index_layer, :, :, field_component_index]
        elif plane == "xz":
            self.X_plot, self.Y_plot = np.meshgrid(self.Z, self.X)
            self.Z_plot = self.Field[:, index_layer, :,  field_component_index]
        #print("sender for update_plot_params", self.sender())
        self.update_plot()

    def update_plot_data(self, position, field):
        x, y, z = [float(i) for i in position.split(",")]
        # give the index in the coordinates
        #print(" update_plot_data:x",x," self.X ",self.X)
        i = np.where(np.isclose(self.X,  x))[0][0]
        #print(" update_plot_data:y",y," self.Y ",self.Y)
        j = np.where(np.isclose(self.Y,  y))[0][0]
        #print(" update_plot_data:z",z," self.Z ",self.Z)
        k = np.where(np.isclose(self.Z,  z))[0][0]
        self.Field[i, j, k] = [float(i) for i in field.split(",")]
        self.update_plot()

    def update_plot(self):
        if self.scan3d_update.isChecked():
            self.update_plot_base()

    def update_plot_type(self):
        if self.scan3d_plottype.currentText() == "quiver":
            self.scan3d_plane.setEnabled(False)
            self.scan3d_layer_slider.setEnabled(False)
            self.scan3d_fieldcomponent.setEnabled(False)
            self.scan3d_layer.setEnabled(False)
            self._ax.set_xlabel("X")
            self._ax.set_ylabel("Y")
            self._ax.set_zlabel("Z")
            self.update_plot()
        else:
            self.scan3d_plane.setEnabled(True)
            self.scan3d_layer_slider.setEnabled(True)
            self.scan3d_fieldcomponent.setEnabled(True)
            self.scan3d_layer.setEnabled(True)
            self.update_layers()
            self.update_field()

    def update_plot_base(self):
        if self.plot_object:
            try:
                self._ax.collections.remove(self.plot_object)
            except:
                # for quiver
                for i in self.plot_object.collections:
                    i.remove()

        if self.scan3d_plottype.currentText() == "surface":
            self.plot_object = self._ax.plot_surface(self.X_plot, self.Y_plot, self.Z_plot, rstride=1, cstride=1, cmap=cm.coolwarm, edgecolor="none")
        elif self.scan3d_plottype.currentText() == "surface and contour":
            self.plot_object = self._ax.plot_surface(self.X_plot, self.Y_plot, self.Z_plot, rstride=1, cstride=1, cmap="viridis", edgecolor="none")
            cset = self._ax.contour(self.X_plot, self.Y_plot, self.Z_plot, zdir='z', offset=self.Z_plot.min(), cmap=cm.coolwarm)
            cset = self._ax.contour(self.X_plot, self.Y_plot, self.Z_plot, zdir='x', offset=self.X_plot.min(), cmap=cm.coolwarm)
            cset = self._ax.contour(self.X_plot, self.Y_plot, self.Z_plot, zdir='y', offset=self.Y_plot.min(), cmap=cm.coolwarm)
        elif self.scan3d_plottype.currentText() == "wireframe":
            self.plot_object = self._ax.plot_wireframe(self.X_plot, self.Y_plot, self.Z_plot,
                                                       rstride=1, cstride=1, cmap=cm.coolwarm)
        elif self.scan3d_plottype.currentText() == "contour":
            self.plot_object = self._ax.contour(self.X_plot, self.Y_plot, self.Z_plot,
                                                cmap=cm.coolwarm)
        elif self.scan3d_plottype.currentText() == "quiver":
            x, y, z = np.meshgrid(self.X, self.Y, self.Z)
            self.plot_object = self._ax.quiver(x, y, z,
                                               self.Field[:, :, :, 0],
                                               self.Field[:, :, :, 1],
                                               self.Field[:, :, :, 2],
                                               length=0.1, normalize=True)

        self.canvas.draw()

############################################################################################################
# The main class
class MainWindow(QMainWindow,Ui_MainWindow):
    AXIS_3D = ["x", "y", "z"]
    PATH_ORDER = ["zxy", "zyx", "yxz", "yzx", "xyz", "xzy"]
    GAUSSMETER_RANGE = ['auto','0','1','2','3','custom']
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # set combobbox values
        self.extrusion_axis.addItems(reversed(self.AXIS_3D))
        self.field_range_x.addItems(self.GAUSSMETER_RANGE)
        self.field_range_y.addItems(self.GAUSSMETER_RANGE)
        self.field_range_z.addItems(self.GAUSSMETER_RANGE)
        self.path.addItems(self.PATH_ORDER)
        self.pathtype_choice.addItems(["mm", "rr"])
        self.direction_choice.addItems(["ppp", "nnn"])
        
        self.volume_nid = 0
        self.path_nid = 0

        # call pyrame
        self.pyrame = Pyrame(self)
        self.pyrame.initModules(pyrame_modules_configuration)

        self.setInitialValues()

        # setting QDoubleValidator for all QLineEdit widgets
        # beware QDoubleValidator depend on locale
        # see https://snorfalorpagus.net/blog/2014/08/09/validating-user-input-in-pyqt4-using-qvalidator/
        double_validator = QDoubleValidator()
        for i in self.findChildren(QLineEdit):
            w = getattr(self, i.objectName())
            w.setValidator(double_validator)
            w.textChanged.connect(self.check_state)
            w.textChanged.emit(w.text())

        for pos_input in ['x_origin', 'y_origin', 'z_origin']:
            w = getattr(self, pos_input)
            w.setEnabled(False)

        for pos_input in ['x_local', 'y_local', 'z_local', 'x_global', 'y_global', 'z_global']:
            w = getattr(self, pos_input)
            w.editingFinished.connect(self.move)

        # Menu bindings
        self.actionLoad_scan_param.triggered.connect(self.loadScanParam)
        self.actionSave_scan_param.triggered.connect(self.saveScanParam)
        self.actionGet_Position.triggered.connect(self.getPositionDebug)
        self.actionGet_Field.triggered.connect(self.getFieldDebug)
        self.actionQuit.triggered.connect(self.exitApplication)

        # connect button to function
        self.x_m.clicked.connect(self.move)
        self.x_p.clicked.connect(self.move)
        self.y_m.clicked.connect(self.move)
        self.y_p.clicked.connect(self.move)
        self.z_m.clicked.connect(self.move)
        self.z_p.clicked.connect(self.move)
        
        self.set_origin.clicked.connect(self.setOrigin)
        self.goto_origin.clicked.connect(self.gotoOrigin)
        self.home.clicked.connect(self.homing)
        
        self.add_current_position.clicked.connect(self.addCurrentPosition)
        self.delete_position.clicked.connect(self.deletePosition)
        self.delete_position.setEnabled(False)
        self.create_volume.clicked.connect(self.createVolume)
        self.create_volume.setEnabled(False)
        self.delete_volume.clicked.connect(self.deleteVolume)
        self.delete_volume.setEnabled(False)
        self.create_path.clicked.connect(self.createPath)
        self.create_path.setEnabled(False)
        self.delete_path.clicked.connect(self.deletePath)
        self.delete_path.setEnabled(False)
        self.save_scan.clicked.connect(self.saveScanParam)
        self.save_scan.setEnabled(False)
        self.start_scan.clicked.connect(self.scan)
        self.start_scan.setEnabled(False)

        self.volume_choice.currentIndexChanged.connect(self.setVolumeParameters)
        self.path_choice.currentIndexChanged.connect(self.setPathParameters)

        # datas for volume and paths
        self.vol_path_3d_data = {
            "volumes": {},
            "paths": {}
            }
        self.path_points = {}
        self.scan_parameters = {}

    def check_state(self, *args, **kwargs):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QValidator.Acceptable:
            color = '#c4df9b' # green
        elif state == QValidator.Intermediate:
            color = '#fff79a' # yellow
        else:
            color = '#f6989d' # red
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def getPositionDebug(self):
        position = []
        for a in self.AXIS_3D:
            retcode, res = self.pyrame.call("get_pos@motions", "axis_%s" % a)
            position.append(res)
        if retcode == 1:
            self.statusbar.showMessage(str(position))
        else:
            self.statusbar.showMessage("Error: cannot get position")

    def getFieldDebug(self):
        r = ''
        for a in self.AXIS_3D:
            cr = getattr(self, "field_range_%s" % a).currentText()[0]  # only the first character means a,0,1,2,3,c
            if cr == 'c':
                cr ='a'
            r += cr
        retcode, res = self.pyrame.call("measure@ls_460", "gaussmeter",r)
        if retcode == 1:
            self.statusbar.showMessage(res)
        else:
            self.statusbar.showMessage("Error: cannot get field")

    def loadScanParam(self):
        name, _ = QFileDialog.getOpenFileName(self, "Load scan file", filter="Scan Files (*.json) ;; All Files (*)", initialFilter='*.json')
        if not name:
            return

        # on devrait commencer par vider l'interface ou alors ajouter les valeurs du fichier au valeur
        # courante mais le problème dans ce cas est d'eviter les doublons
        self.vol_path_3d_data = json.loads(open(name).read())

        self.volume_choice.blockSignals(True)
        for vol_id in self.vol_path_3d_data["volumes"]:
            self.volume_choice.addItem(vol_id)
        self.volume_choice.blockSignals(False)

        self.path_choice.blockSignals(True)
        for path_id in self.vol_path_3d_data["paths"]:
            self.path_choice.addItem(path_id)
        self.path_choice.blockSignals(False)

        # update GUI buttons
        self.create_volume.setEnabled(True)
        self.delete_volume.setEnabled(True)
        self.create_path.setEnabled(True)
        self.delete_path.setEnabled(True)
        self.save_scan.setEnabled(True)
        self.start_scan.setEnabled(True)
        self.delete_position.setEnabled(True)
        self.set_origin.setEnabled(False)

        # update the GUI  using the path given o
        # self.path_choice.addItem(path_id)
        if self.vol_path_3d_data["paths"]:
            self.setPathParameters()

        
    def saveScanParam(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save scan file', filter="Scan Files (*.json) ;; All Files (*)", initialFilter='*.json')
        if name:
            print(self.vol_path_3d_data)
            with open(name, 'w') as file:
                file.write(json.dumps(self.vol_path_3d_data, indent=4))

    def exitApplication(self):
        """
        Clean up on exit
        """
        button = QMessageBox.question(self,
                                      "Quit",
                                      "Are you sure you want to quit?",
                                      buttons=QMessageBox.Yes | QMessageBox.No,
                                      defaultButton=QMessageBox.Yes,
                                      )

        if button == QMessageBox.Yes:
            # removing space, volume and paths ids
            # we should also remove paths and volumes
            #self.pyrame.call("deinit_space@paths", "space_1")
            #for i in range(self.volume_choice.count()):
            #    print(self.volume_choice.itemText(i))
            #    self.pyrame.call("deinit_volume@paths",self.volume_choice.itemText(i))
            #for i in range(self.path_choice.count()):
            #    self.pyrame.call("deinit_path@paths",self.path_choice.itemText(i))
            
            self.pyrame.deinitModules()
            self.close()

    def updatePositionWidget(self, values=None):
        if values:
            p = values.split(",")
        else:
            p = []
            for a in self.AXIS_3D:
                print("self.pyrame type: ", type(self.pyrame))
                retcode, res = self.pyrame.call("get_pos@motion", "axis_%s" % a)
                if retcode == 1:
                    p.append(res)
                else:
                    return
        for a, c in zip(self.AXIS_3D, p):
            w = getattr(self, "%s_global" % a )
            w.setText(c)
                        
            w = getattr(self, "%s_origin" % a)
            o = float(w.text())
            w = getattr(self, "%s_local" % a)
            w.setText(str(float(c) - o))

    def updateGaussmeterWidget(self, values=None):
        if values == None:
            r = ""
            for a in self.AXIS_3D:
                cr = getattr(self, "field_range_%s"% a).currentText()[0]  # only the first character means a,0,1,2,3,c
                if cr == 'c':
                    cr ='a'
                r += cr
            retcode, res = self.pyrame.call("measure@ls_460", "gaussmeter",r)
            if retcode == 1:
                Bx, By, Bz, Bn =res.split(",")
            else:
                return
        else:
            Bx, By, Bz, Bn = values.split(",")

        self.field_x.setText(Bx)
        self.field_y.setText(By)
        self.field_z.setText(Bz)
        self.field_norm.setText(Bn)

    def setInitialValues(self):
        """
        init interface with value in a conf file or internal data and by querying the devices
        :return:
        """
        for w, v in initial_values.items():
            getattr(self, w).setText(v)

        self.updatePositionWidget()
        self.updateGaussmeterWidget()

    def move(self):
        # les boutons et TextField qui peuvent qppeler cette methode on comme
        # noms {x,y,z}_{p,m} pour les boutons de plus et de moins
        # noms {x,y,z}_{local,global} pour les TextField  de plus et de moins

        axis, suffix = self.sender().objectName().split("_")
        axis_index = self.AXIS_3D.index(axis)

        speed = getattr(self, "%s_speed" % axis).text()
        acc = getattr(self, "%s_acc" % axis).text()

        if suffix in ["p", "m"]:
            step = float(getattr(self, "%s_step" % axis).text())
            if suffix == "m":
                step = -step
        elif suffix in ["local", "global"]:
            # comme on ne connait pas la différence entre la position courante et la position demandée il faut
            # récupérer  la valeur courante pour calculer la différence
            retcode, res = self.pyrame.call("get_pos@motions", "axis_%s" % axis)
            curr_pos = float(res)
            if suffix == "local":
                local_pos = getattr(self, "%s_local" % axis).text()
                origin = getattr(self, "%s_origin" % axis).text()
                pos = float(local_pos)+float(origin)
            else:
                pos = float(getattr(self, "%s_global" % axis).text())
            step = str(pos - curr_pos)

        print("move: axis %s step %s speed %s acc %s" % (axis, step, speed, acc))
        retcode, res = self.pyrame.call("move@motion","axis_%s" % axis, step, speed, acc)
        if retcode == 1:
            self.updatePositionWidget()

    def setOrigin(self):
        for axis in self.AXIS_3D:
            g = getattr(self, "%s_global" % axis).text()
            getattr(self, "%s_origin" % axis).setText(g)
            getattr(self, "%s_local" % axis).setText("0.0")

    def gotoOrigin(self):
        dlg = orderedMovement_Dialog()
        dlg.explanation.setText("Order axis for Goto Origin")
        dlg.orderCombo.addItems(self.PATH_ORDER)
        if dlg.exec_():
            for d in dlg.orderCombo.currentText():
                ep = float(getattr(self, "%s_origin" % d).text())
                cp = float(getattr(self, "%s_global" % d).text())
                s = getattr(self, "%s_speed" % d).text()
                a = getattr(self, "%s_acc" % d).text()
                #print("moving axis %s to position %s with speed %s and acc %s" % (d, str(ep -cp) ,v,a))
                retcode, res = self.pyrame.call("move@motion", "axis_%s" % d,str(ep-cp),s,a)
                if retcode == 1:
                   self.updatePositionWidget()

    def homing(self):
        dlg = orderedMovement_Dialog()
        dlg.explanation.setText("Order axis for Homing. Check twice !!")
        dlg.orderCombo.addItems(self.PATH_ORDER+["x", "y", "z"])
        if dlg.exec_():
            for d in dlg.orderCombo.currentText():          
                retcode, res = self.pyrame.call("home@motion", "axis_%s" % d, "r", "1")
                if retcode == 1:
                    self.updatePositionWidget()
       
    def addCurrentPosition(self):
        """
        Add the current point in the list of points of interest. Note we run on local coordinates from now
        """
        # set the interface 
        self.delete_position.setEnabled(True)
        self.set_origin.setEnabled(False)
        self.create_volume.setEnabled(True)

        # set the local position in the points_3D widget
        coord = ",".join([getattr(self, "%s_local" % axis).text() for axis in self.AXIS_3D])
        if not self.points_3d.findItems(coord, Qt.MatchExactly):
            self.points_3d.addItem(coord)
                        
    def deletePosition(self):
        for i in self.points_3d.selectedItems():
            self.points_3d.takeItem(self.points_3d.row(i))

        # we update the interface when all the points in the list are deleted
        if self.points_3d.count() == 0:
            self.delete_position.setEnabled(False)
            self.create_volume.setEnabled(False)
            self.set_origin.setEnabled(True)

    def createVolume(self):
        # on récupére les données de l'interface pour décrire le volume

        ext_axis = self.extrusion_axis.currentText()
        ext_axis_start = float(getattr(self, "min_extrusion").text())
        ext_axis_end = float(getattr(self, "max_extrusion").text())

        origin = np.array([float(getattr(self, "%s_origin" % a).text()) for a in self.AXIS_3D])

        points = []
        for p in range(self.points_3d.count()):
            points.append([float(i) for i in self.points_3d.item(p).text().split(",")])

        points = np.array(points) + origin

        # dans le polyhedre définit par l'extrusion l'axe d'extrusion est note Z
        # la matrice de transformation est
        plot_boundaries = np.ndarray([3, 2])
        if ext_axis == "x":
            coord_m = [1, 2, 0]
        elif ext_axis == "y":
            coord_m = [2, 0, 1]
        elif ext_axis == "z":
            coord_m = [0, 1, 2]

        X, Y, Z = coord_m
        plot_boundaries[Z] = [min(ext_axis_end, ext_axis_start), max(ext_axis_end, ext_axis_start)]
        plot_boundaries[X] = [min(points[:, X]), max(points[:, X])]
        plot_boundaries[Y] = [min(points[:, Y]), max(points[:, Y])]
        polygon_points = points[:, [X, Y]]
        
        # we need to ask for a name for the vol_id
        dlg = askForName()
        dlg.message.setText("Enter volume id")
        dlg.lineEditField.setText("vol_%d" % self.volume_nid)
        if dlg.exec_():
            vol_id = dlg.lineEditField.text()
            if not self.vol_path_3d_data["volumes"].get(vol_id):
                self.vol_path_3d_data["volumes"][vol_id] = {
                    "coord_m": coord_m,
                    "extrusion_axis": ext_axis,
                    "extrusion_limits": plot_boundaries[Z],
                    "origin": origin.tolist(),
                    "points": points.tolist(),
                    "polygon_points": polygon_points.tolist(),
                    "plot_boundaries": plot_boundaries.tolist()
                }
                self.save_scan.setEnabled(True)
                self.create_path.setEnabled(True)
                self.delete_volume.setEnabled(True)
                self.volume_nid += 1
                
                # avoid triggering the programmatic change of the Qcombobox volume_choice
                self.volume_choice.blockSignals(True)
                self.volume_choice.addItem(vol_id)
                self.volume_choice.setCurrentText(vol_id)
                self.volume_choice.blockSignals(False)

    def deleteVolume(self):
        vol_id = self.volume_choice.currentText()
        self.volume_choice.blockSignals(True)
        index = self.volume_choice.findText(vol_id)
        self.volume_choice.removeItem(index)
        self.volume_choice.blockSignals(False)

        # update interface if there is no volume to delete anymore
        if self.volume_choice.count() == 0:
            self.delete_volume.setEnabled(False)
            self.create_path.setEnabled(False)
        # remove from dict
        self.vol_path_3d_data["volumes"].pop(vol_id)
        # we need to find the path associated with the volume and remove them
        path_id_to_remove = [p[0] for p in self.vol_path_3d_data["paths"].items() if p[1]['vol_id'] == vol_id]
        for p in path_id_to_remove:
            self._deletePath(p)

    def setVolumeParameters(self):
        vol_id = self.volume_choice.currentText()
        vol_data = self.vol_path_3d_data["volumes"][vol_id]
        for d, v in zip(self.AXIS_3D, vol_data["origin"]):
            getattr(self, "%s_origin" % d).setText(str(v))
            g = getattr(self, "%s_global" % d).text()
            getattr(self, "%s_local" % d).setText(str(v-float(g)))
        self.points_3d.clear()
        self.points_3d.addItems([",".join(["%s" % c for c in p]) for p in vol_data["points"]])

        # on teste si le path_id courant contient le vol_id si oui alors on ne fait rien sinon
        # on modifie les paths

        path_id = self.path_choice.currentText()
        if self.vol_path_3d_data["paths"][path_id]["vol_id"] == vol_id:
            return
        else:
            list_of_paths = []
            for p in self.vol_path_3d_data["paths"].items():
                if p[1]["vol_id"] == vol_id:
                    list_of_paths.append(p[0])
            if list_of_paths:
                self.path_choice.blockSignals(True)
                self.path_choice.clear()
                self.path_choice.addItems(list_of_path)
                self.path_choice.blockSignals(False)
                self.setPathParameters()

    def createPath(self):
        map_xyzton={
            "x": "1",
            "y": "2",
            "z": "3"
        }

        vol_id = self.volume_choice.currentText()
        path_order = "".join([map_xyzton[i] for i in self.path.currentText()])
        
        steps = [
            float(self.scan_x_step.text()),
            float(self.scan_y_step.text()),
            float(self.scan_z_step.text())
        ]

        dlg = askForName()
        dlg.message.setText("Enter path id")
        dlg.lineEditField.setText("path_%d" % self.path_nid)
        if dlg.exec_():
            path_id = dlg.lineEditField.text()
            path_type = self.pathtype_choice.currentText()
            path_directions = self.direction_choice.currentText()

            self.vol_path_3d_data["paths"][path_id] = {
                "vol_id": vol_id,
                "path_order": path_order,
                "steps": steps,
                "path_type": path_type,
                "path_directions": path_directions
            }

            self.start_scan.setEnabled(True)
            self.delete_path.setEnabled(True)
            self.path_nid += 1
            self.path_choice.addItem(path_id)
            # avoid triggering the programmatic change of the Qcombobox volume_choice
            self.path_choice.blockSignals(True)
            self.path_choice.setCurrentText(path_id)
            self.path_choice.blockSignals(False)
            #self.nb_plot_points = float(res.split(":")[0])


    def deletePath(self):
        #print("deletePath:self.sender:", self.sender())
        path_id = self.path_choice.currentText()
        self._deletePath(path_id)

    def _deletePath(self, path_id):
        # print("_deletePath:path_id", path_id)
        retcode, res = self.pyrame.call("deinit_path@paths", path_id)
        if retcode == 1:
            self.path_choice.blockSignals(True)
            index = self.path_choice.findText(path_id)
            self.path_choice.removeItem(index)
            self.path_choice.blockSignals(False)

            if self.path_choice.count() == 0:
                self.delete_path.setEnabled(False)
                self.start_scan.setEnabled(False)

            self.vol_path_3d_data["paths"].pop(path_id)

    def setPathParameters(self):
        # print("setPathParameters called")
        path_id = self.path_choice.currentText()
        path_data = self.vol_path_3d_data["paths"][path_id]
        self.scan_x_step.setText(str(path_data["steps"][0]))
        self.scan_y_step.setText(str(path_data["steps"][1]))
        self.scan_z_step.setText(str(path_data["steps"][2]))
        self.pathtype_choice.setCurrentText(path_data["path_type"])
        self.direction_choice.setCurrentText(path_data["path_directions"])
 
        vol_id = path_data["vol_id"]
        print("setPathParameters: vol_id", vol_id,self.volume_choice.currentText())
        # si le volume courant est celui du path_id alors on ne fait rien sinon on met à jour
        if self.volume_choice.currentText() == vol_id:
            return
        # TODEBUG self.volume_choice.setCurrentText(vol_id) should trigger self.setVolumeParameters()
        self.volume_choice.setCurrentText(vol_id)
        self.setVolumeParameters()
        
    def reportField(self):
        self.plot_point_index += 1
        #p, f = n.split(";")
        # updating the widget set he value of position and field in the interface
        self.scan3d_plot.scan3d_progress.setValue(100.*self.plot_point_index/self.nb_plot_points)
        current_time = time.time()
        remaining_time = (current_time - self.scan3d_plot_time_previous_step) * (self.nb_plot_points-self.plot_point_index)
        self.scan3d_plot.scan3d_timeleft.setText("%ss" % int(remaining_time))
        self.scan3d_plot_time_previous_step = current_time
        #self.updatePositionWidget()
        #self.updateGaussmeterWidget()

        # update plot
        p = "%s,%s,%s" % (self.x_global.text(),self.y_global.text(),self.z_global.text())
        f = "%s,%s,%s,%s" % (self.field_x.text(),self.field_y.text(),self.field_z.text(),self.field_norm.text())

        self.scan3d_plot.update_plot_data(p, f)
        # write datafile

        self.data_file.write("0\t0\t")
        self.data_file.write("\t%s" % p.replace(",", "\t"))
        self.data_file.write("\t%s" % self.x_local.text())
        self.data_file.write("\t%s" % self.y_local.text())
        self.data_file.write("\t%s" % self.z_local.text())
        self.data_file.write("\t%s" % f.replace(",", "\t"))
        self.data_file.write("\t%s" % datetime.now().strftime("%Y%m%d"))
        self.data_file.write("\t%d" % int(time.time() - self.start_acq_time))
        self.data_file.write("\taaa\n")


    def scan3d_finished_scan(self):
        self.scan3d_plot.scan3d_stop.setText("Close")
        self.scan3d_plot.scan3d_suspend.setEnabled(False)
        # close data file
        self.data_file.close()

    def scan(self):
        path_id = self.path_choice.currentText()

        # on initialize le calcul.
        self.computePath()
        self.nb_plot_points = self.path_points[path_id].shape[0]
        move_params = []
        strategy = ["undef"]
        speed = []
        acc = []

        for a in self.AXIS_3D:
            speed.append(getattr(self, "%s_speed" % a).text())
            acc.append(getattr(self, "%s_acc" % a).text())

        move_params.extend(speed)
        move_params.extend(acc)
        move_params.extend(strategy)

        self.thread = QThread()

        self.worker = Worker(self.path_points[path_id], move_params, self.pyrame, self)

        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)

        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.finished.connect(self.scan3d_finished_scan)
        self.worker.field.connect(self.reportField)

        # open data file
        self.open_data_filename()
        self.start_acq_time = time.time()
        self.plot_point_index = 0

        # Step 6: Start the thread
        self.thread.start()


        self.scan3d_plot = Scan3dPlotDialog(self.worker)
        self.scan3d_plot.init_plot_data(self.scan_parameters[path_id])
        self.scan3d_plot.show()
        self.scan3d_plot.scan3d_nbpoints.setText(str(self.nb_plot_points))
        self.scan3d_plot_time_previous_step = time.time()
        self.thread.start()

    def open_data_filename(self):
        DATADIR = "/root/Gaussmeter/Data/"
        data_prefix = "gaussbench_data"
        data_filename = "%s%s%s" % (DATADIR,data_prefix,datetime.now().strftime("%Y_%m_%d_%H.%M"))

        name, _ = QFileDialog.getSaveFileName(self, 'Scan Data file', directory=data_filename)
        print("filename :",name)

        if name:
            self.data_file = open(name, "w", 1)
            # the header
            self.data_file.write("# units are Tesla, degrees, mm and s\n")
            self.data_file.write("# Local coordinate system origin: x0=%s, y0=%s, z0=%s\n" % (self.x_origin.text(),self.y_origin.text(),self.z_origin.text()))
            retcode, res = self.pyrame.call("free_query@ls_460","gaussmeter","SNUM?")
            if retcode == 1:
                self.data_file.write("# gaussmeter probe %s \n" % res)
            else:
                self.data_file.write("# gaussmeter probe ERROR %s \n" % res)
            self.data_file.write("# mag ang probe ang\tx glob\ty glob\tz glob\tx local\ty local\tz local\tX Bfield\tY Bfield\tZ Bfield\tV Bfield\tdate\telapsed time\trange\n")

    def computePath(self):
        """
        Calcule le chemim que doit décrire le setup pour mesurer l'aimant
        :return:
        """

        # on récupére les paramètres de l'interface ainsi que ceux du dictionnaire pour
        # construire le chemin
        pprint(self.vol_path_3d_data, depth=3)
        path_id = self.path_choice.currentText()

        # si on à déjà calculé ce chemin on ne fait rien.
        if self.path_points.get(path_id):
            return
        print("path_id: ", path_id,self.path_choice.count())
        vol_id = self.vol_path_3d_data["paths"][path_id]["vol_id"]

        poly_coords = np.array(self.vol_path_3d_data["volumes"][vol_id]["polygon_points"])
        ext_axis = self.vol_path_3d_data["volumes"][vol_id]["extrusion_axis"]
        ext_limits = self.vol_path_3d_data["volumes"][vol_id]["extrusion_limits"]
        steps = self.vol_path_3d_data["paths"][path_id]["steps"]
        path_order = self.vol_path_3d_data["paths"][path_id]["path_order"]
        path_type = self.vol_path_3d_data["paths"][path_id]["path_type"]
        path_directions = self.vol_path_3d_data["paths"][path_id]["path_directions"]
        plot_boundaries = self.vol_path_3d_data["volumes"][vol_id]["plot_boundaries"]
        self.path_points[path_id] = paths.generate_path(poly_coords, ext_axis, ext_limits,
                                                   steps,
                                                   path_order, path_type, path_directions)
        data_structure = []
        for i in range(3):
            pb_1 = plot_boundaries[i][1]
            pb_0 = plot_boundaries[i][0]
            N = int((10.*pb_1 - 10*pb_0) / (10.*steps[0])) + 1
            data_structure.extend([N, pb_1, pb_0])
            
        self.scan_parameters[path_id] = data_structure
        


import click
@click.command()
@click.option("--simulate", is_flag=True, help="simulate the device")
def main(simulate):
    global SIMULATE
    print(simulate)
    SIMULATE = simulate
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
