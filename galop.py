#! coding: utf-8

import sys,time
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QWidget,
    QDialogButtonBox,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel,
    QMessageBox,
    QFileDialog,
    QLineEdit,
    QComboBox
)
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer

module_to_start = """
cmdmod /opt/pyrame/cmd_serial.xml &
cmdmod /opt/pyrame/cmd_gpib.xml &
cmdmod /opt/pyrame/cmd_th_apt.xml &
cmdmod /opt/pyrame/cmd_motion.xml &
cmdmod /opt/pyrame/cmd_paths.xml &
cmdmod /opt/pyrame/cmd_ls_460.xml &
"""
_Nx, _Xi, _Xf, _Ny, _Yi, _Yf, _Nz, _Zi, _Zf = 10, -1, 1, 10, 0, 2, 10, -3, -1

import json
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator,QValidator

from galop_ui import Ui_MainWindow
from scan3d_ui import Ui_Dialog
from scan3dwidget_ui import Ui_Form

import bindpyrame

# datas should be taken from a file
initial_values = {
    "x_origin" : "0.0",
    "x_step": "1.0",
    "x_acc": "2",
    "x_speed": "2",
    "y_origin" : "0.0",
    "y_step": "1.0",
    "y_acc": "2",
    "y_speed": "2",
    "z_origin" : "0.0",
    "z_step": "1.0",
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
            "paths"
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
#    "multimeter": {
#        "gaussmeter": {
#            "init": [
#                "ls_460(bus=gpib(bus=serial(vendor=0403,product=6001,timeout=10),dst_addr=12),Bunits=T,Bmode=0,Bfilter=0,nb_channels=3)"],
#            "config": []
#        },
#    },
    "ls_460": {
        "gaussmeter": {
            "init": [
                "ls_460(bus=gpib(bus=serial(vendor=0403,product=6001,timeout=10),dst_addr=12),Bunits=T,Bmode=0,Bfilter=0,nb_channels=3)"],
            "config": []
        },
    },
    "paths": {
        "space_1": {
            "init_order": ["init_space"],
            "deinit_order": ["deinit_space"],
            "init_space": ["axis_x", "axis_y", "axis_z", "0.1", "0.1", "0.1"]
        }
    }
}


class Pyrame(object):
    def __init__(self,parent):
        self.module_port = {}
        self.parent = parent

     # Pyrame Stuff
    def initModules(self,pyrame_modules_configuration):
        # read conf file
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
        # we inval and deinit the modules
        for module, values in self.pyrame_modules_init.items():
            for uid, params in values.items():
                order = params.get('deinit_order', ["inval","deinit"])
                for function in order:
                         retcode, res = self.call(
                             "%s@%s" % (function, module),
                             uid
                         )

    def call(self, pyrame_func, *args):
        """
        Function to call pyrame module and prevent user action. Inform user in case of error

        :param pyrame_func: the pyrame function to call in the form function@module
        :param args: the args of the function
        :return: the return of the pyrame module
        """
        
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

# thread for scan
class MUWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    field = pyqtSignal(str)

    def __init__(self, move_params, pyrame):
        super().__init__()
        self._isrunning = True
        self.pyrame = pyrame
        self.move_params = move_params
        self._issuspended = False

    def run(self):
        lx, ly, lz = _Nx, _Ny, _Nz
        nb_points = lx*ly*lz
        xi, xf = _Xi, _Xf
        yi, yf = _Yi, _Yf
        zi, zf = _Zi, _Zf
        i = 0
        while self._isrunning:
            if not self._issuspended:
                i_z = int(i/(1.*ly*lx))
                i_y = int((i-i_z*lx*ly)/(1.*lx))
                i_x = int((i-i_z*lx*ly-i_y*lx))
                x = xi+(xf-xi)/(lx-1.)*float(i_x)
                y = yi+(yf-yi)/(ly-1.)*float(i_y)
                z = zi+(zf-zi)/(lz-1.)*float(i_z)
                #bx = -np.sin((x-z) ** 2 + y ** 2) / 10.
                #by = (16. * x * (1-x) * y * (1-y) * np.sin(9 * np.pi * x) * np.sin(9 * np.pi * y))**2
                #bz = x*np.exp(-((x-z)**2+y**2))
                bx = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
                by = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
                bz = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) * np.sin(np.pi * z))
                bn = np.sqrt(bx*bx + by*by + bz*bz)
                position = "%f,%f,%f" % (x, y ,z)
                field = "%f,%f,%f,%f" % (bx, by, bz , bn
                                         )
                print("In worker ", x,y,z,i,i_x+i_y*lx+i_z*lx*lz)
                self.field.emit("%s;%s" % (position, field))
                self.progress.emit(100.*i/(nb_points-1))
                i += 1
                if i == nb_points:
                    self._isrunning = False
                time.sleep(0.1)

        self.finished.emit()

    def stop(self):
        self._isrunning = False

    def suspend(self):
        self._issuspended = not self._issuspended


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    field = pyqtSignal(str)

    def __init__(self, move_params, pyrame):
        super().__init__()
        self.pyrame = pyrame
        self.move_params = move_params

    def run(self):

        retcode, res = self.pyrame.call("move_first@paths", *self.move_params)
        retcode, position = self.pyrame.call("get_position@paths", "space_1")
        retcode, field = self.pyrame.call("measure@ls_460", "gaussmeter")

        # create file and start writing it
        print("data", position, field)
        self.field.emit("%s;%s" % (position, field))

        run = True
        while run:
            retcode, res = self.pyrame.call("move_next@paths", *self.move_params)
            retcode, position = self.pyrame.call("get_position@paths", "space_1")
            retcode, field = self.pyrame.call("measure@ls_460", "gaussmeter")
            print("data", position, field)
            self.field.emit("%s;%s" % (position, field))
            if res == "finished":
                run = False

        self.finished.emit()


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
class Scan3dPlotWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Scan3dPlotWidget,self).__init__(parent)
        self.setupUi(self)
        self.stop.clicked.connect(self.close)


# 3D scan class
class Scan3dPlotDialog(QDialog, Ui_Dialog):
    def __init__(self, working_thread, parent=None):
        super(Scan3dPlotDialog, self).__init__(parent)
        self.working_thread = working_thread

        self.setupUi(self)

        #self.fig = Figure(figsize=(5, 3))
        #self.canvas = FigureCanvas(self.fig)
        #self.widget = self.canvas
        #self.fig=self.widget.fig
        #self.canvas = self.widget.canvas


        self.scan3d_stop.clicked.connect(self.stop)
        self.scan3d_suspend.clicked.connect(self.suspend)
        self.scan3d_update.setChecked(True)
        self.scan3d_plane.addItems(["xy", "yz", "xz"])
        self.scan3d_fieldcomponent.addItems(["Bx","By","Bz","B norm"])
#        self.scan3d_plottype.addItems(["surface","surface and contour","wireframe"])
        self.scan3d_plottype.addItems(["surface", "wireframe", "quiver"])

        self.scan3d_plottype.currentTextChanged.connect(self.update_plot_base)
        self.scan3d_plane.currentTextChanged.connect(self.update_layers)
        self.scan3d_layer.currentTextChanged.connect(self.update_plot_params)
        self.scan3d_fieldcomponent.currentTextChanged.connect(self.update_field)

        #self.fig.set_canvas(self.canvas)
        self._ax = self.canvas.figure.add_subplot(projection="3d")
        self._ax.view_init(30, 30)
        self.plot_object = None


    def stop(self):
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
        self.Field = np.ndarray([nx, ny, nz, 4])
        self.X = np.linspace(xi, xf, nx)
        self.Y = np.linspace(yi, yf, ny)
        self.Z = np.linspace(zi, zf, nz)
        self.all_elements = nx*ny*nz
        self.update_layers()
        self.update_plot_params()

    def update_field(self):
        self._ax.set_zlabel(self.scan3d_fieldcomponent.currentText())
        self.update_plot_params()

    def update_layers(self):
        plane = self.scan3d_plane.currentText()
        self.scan3d_layer.clear()
        if plane == "xy":
            self.scan3d_layer.addItems([str(i) for i in self.Z])
            self._ax.set_xlabel("Y")
            self._ax.set_ylabel("X")
        elif plane == "yz":
            self.scan3d_layer.addItems([str(i) for i in self.X])
            self._ax.set_xlabel("Z")
            self._ax.set_ylabel("Y")
        elif plane == "xz":
            self.scan3d_layer.addItems([str(i) for i in self.Y])
            self._ax.set_xlabel("Z")
            self._ax.set_ylabel("X")
        self.update_plot_params()

    def update_plot_params(self):
        plane = self.scan3d_plane.currentText()
        index_layer = self.scan3d_layer.currentIndex()
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
        print(self.X_plot.shape,self.Y_plot.shape,self.Z_plot.shape)
        self.update_plot()

    def update_plot_data(self,position,field):
        x, y, z = [float(i) for i in position.split(",")]
        # give the index in the coordinates
        #print(x,self.X,np.where(np.isclose(self.X,  x)))
        i = np.where(np.isclose(self.X,  x))[0][0]
        j = np.where(np.isclose(self.Y,  y))[0][0]
        k = np.where(np.isclose(self.Z,  z))[0][0]
        self.Field[i, j, k] = [float(i) for i in field.split(",")]
        self.update_plot()

    def update_plot(self):
        if self.scan3d_update.isChecked():
            self.update_plot_base()

    def update_plot_base(self):
        print("updating plot base")
        if self.plot_object:
            self._ax.collections.remove(self.plot_object)
        if self.scan3d_plottype.currentText() == "surface":
            self.plot_object = self._ax.plot_surface(self.X_plot, self.Y_plot, self.Z_plot, rstride=1, cstride=1, cmap="viridis", edgecolor="none")
        #elif self.scan3d_plottype.currentText() == "surface and contour":
        #    self.plot_object = self._ax.plot_surface(self.X_plot, self.Y_plot, self.Z_plot, rstride=1, cstride=1, cmap="viridis", edgecolor="none")
        #    cset = self._ax.contour(self.X_plot, self.Y_plot, self.Z_plot, zdir='z', offset=self.Z_plot.min(), cmap=cm.coolwarm)
        #    cset = self._ax.contour(self.X_plot, self.Y_plot, self.Z_plot, zdir='x', offset=self.X_plot.min(), cmap=cm.coolwarm)
        #    cset = self._ax.contour(self.X_plot, self.Y_plot, self.Z_plot, zdir='y', offset=self.Y_plot.min(), cmap=cm.coolwarm)
        elif self.scan3d_plottype.currentText() == "wireframe":
            self.plot_object = self._ax.plot_wireframe(self.X_plot, self.Y_plot, self.Z_plot,rstride=1, cstride=1, cmap="viridis")
        elif self.scan3d_plottype.currentText() == "quiver":
            x,y,z = np.meshgrid(self.X, self.Y, self.Z)
            print(x.shape,y.shape,z.shape,self.Field[:, :, :, 0].shape)
            self.plot_object = self._ax.quiver(x,y,z,
                                               self.Field[:, :, :, 0],
                                               self.Field[:, :, :, 1],
                                               self.Field[:, :, :, 2],
                                               length=0.1, normalize=True)

        self.canvas.draw()



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
        
        self.volume_nid = 0
        self.path_nid = 0
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
        self.start_scan.clicked.connect(self.scan)
        #self.start_scan.setEnabled(False)

        # datas
        self.vol_path_3d_data = {}
        self.scan()

        
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

    def loadScanParam(self):
        name, _ = QFileDialog.getOpenFileName(self, "Load scan file")
        print(json.loads(open(name)))
        # need to create vol and path from there. This mean updating the interface and click or execute directly the functions.
        # the problem is how do we know the coordinates of the point since they can change from one volume to another.
        # or shall we go from position to path in one click hiding the volume part?

    def saveScanParam(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save scan file', filter="Scan Files (*.json) ;; All Files (*)", initialFilter='*.json')
        with open(name, 'w') as file:
            file.write(json.dumps(self.vol_path_3d_data))

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
            self.pyrame.call("deinit_space@paths","space_1")
            for i in range(self.volume_choice.count()):
                print(self.volume_choice.itemText(i))
                self.pyrame.call("deinit_volume@paths",self.volume_choice.itemText(i))
            for i in range(self.path_choice.count()):
                self.pyrame.call("deinit_path@paths",self.path_choice.itemText(i))
            
            self.pyrame.deinitModules()
            self.close()

    def updatePositionWidget(self, values=None):
        if values:
            p = values.split(",")
        else:
            retcode, res = self.pyrame.call("get_position@paths", "space_1")
            if retcode == 1:
                p = res.split(',')
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
                cr = getattr(self,"field_range_%s"% a).currentText()[0]  # only the first character means a,0,1,2,3,c
                if cr=='c':
                    cr ='a'
                r += cr
            retcode, res = self.pyrame.call("measure@ls_460", "gaussmeter",r)
            if retcode == 1:
                Bx, By, Bz, Bn =res.split(",")
        else:
            retcode = 1
            Bx, By, Bz, Bn = values.split(",")
        if retcode == 1:
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
        # extract axis and direction from the button name

        pos = []
        speed = []
        acc = []
        for a in self.AXIS_3D:
            pos.append(getattr(self, "%s_global" % a).text())
            speed.append(getattr(self, "%s_speed" % a).text())
            acc.append(getattr(self, "%s_acc" % a).text())

        axis, suffix = self.sender().objectName().split("_")
        axis_index = self.AXIS_3D.index(axis)

        if suffix == "local":
            pos[axis_index] = "%f" % (float(getattr(self, "%s_local" % axis).text()) + float(getattr(self, "%s_origin" % axis).text()))
        elif suffix in ["p","m"]:
            step = float(getattr(self, "%s_step" % axis).text())
            if suffix == "m":
                step = -step
            pos[axis_index] = "%f" % (float(getattr(self, "%s_global" % axis).text())+step)

        print("moving to pos",pos)
        retcode, res = self.pyrame.call("move_space@paths","space_1",*(pos+speed+acc))
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
            print("Done", dlg.scan_order)
            #for a in dlg.scan_order:
            #    getattr(self, "%s_global" % a).setText(getattr(self, "%s_origin" % a).text())

    def homing(self):
        dlg = orderedMovement_Dialog()
        dlg.explanation.setText("Order axis for Homing. Check twice !!")
        dlg.orderCombo.addItems(self.PATH_ORDER+["x","y","z"])
        if dlg.exec_():
            for d in dlg.orderCombo.currentText():          
                retcode, res = self.pyrame.call("home@motion", "axis_%s" % d,"r","1")
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
        ext_axis = self.extrusion_axis.currentText()
        if ext_axis == "x":
            c0, c1, c2 = 1, 2, 0
        elif ext_axis == "y":
            c0, c1, c2 = 0, 2, 1
        elif ext_axis == "z":
            c0, c1, c2 = 0, 1, 2

        origin = []
        for a in self.AXIS_3D:
            origin.append(float(getattr(self, "%s_origin" % a).text()))

        axis_min = float(getattr(self, "min_extrusion").text())
        axis_max = float(getattr(self, "max_extrusion").text())
        new_coords = ""
        all_coords = []
        for i in range(self.points_3d.count()):
            coords = self.points_3d.item(i).text().split(',')
            all_coords.append(coords)
            new_coords += "%s,%s;" % (float(coords[c0]) + origin[c0],float(coords[c1]) + origin[c1])
            
        coords = self.points_3d.item(0).text().split(',')
        all_coords.append(coords)
        new_coords += "%s,%s;" % (float(coords[c0]) + origin[c0],float(coords[c1]) + origin[c1])

        # we need to ask for a name for the vol_id
        dlg = askForName()
        dlg.message.setText("Enter volume id")
        dlg.lineEditField.setText("vol_%d" % self.volume_nid)
        if dlg.exec_():
            vol_id = dlg.lineEditField.text()
            retcode, res = self.pyrame.call("init_volume@paths",
                                           vol_id,
                                           "space_1",
                                           "prism",
                                           "prism",
                                           new_coords,
                                           ext_axis,
                                           "%s" % (axis_min+origin[c2]),
                                           "%s" % (axis_max+origin[c2]))
            if retcode == 1:
                self.vol_path_3d_data["volumes"]={
                    vol_id: {
                        "origin": origin,
                        "ext_axis": ext_axis,
                        "axis_min": axis_min,
                        "axis_max": axis_max,
                        "all_coords": all_coords
                        }
                }
                self.create_path.setEnabled(True)
                self.delete_volume.setEnabled(True)
                self.volume_nid += 1
                self.volume_choice.addItem(vol_id)
                self.volume_choice.setCurrentText(vol_id)

    def deleteVolume(self):
        vol_id = self.volume_choice.currentText()
        retcode, res = self.pyrame.call("deinit_volume@paths",vol_id)
        if retcode == 1:
            self.volume_choice.removeItem(self.volume_choice.currentIndex())

            # update interface if there is no volume to delete anymore
            if self.volume_choice.count() == 0:
                self.delete_volume.setEnabled(False)
                self.create_path.setEnabled(False)

    def createPath(self):
        map_xyzton={"x":"1","y":"2","z":"3"}

        vol_id = self.volume_choice.currentText()
        path_order = "".join([map_xyzton[i] for i in self.path.currentText()])
        
        scan_x_step = self.scan_x_step.text()
        scan_y_step = self.scan_y_step.text()
        scan_z_step = self.scan_z_step.text()

        dlg = askForName()
        dlg.message.setText("Enter path id")
        dlg.lineEditField.setText("path_%d" % self.path_nid)
        if dlg.exec_():
            path_id = dlg.lineEditField.text()
            path_type = "rr"
            path_directions = "ppp"
            retcode,res = self.pyrame.call("init_path@paths",path_id,"space_1",vol_id,scan_x_step,scan_y_step,scan_z_step,path_order,path_type,path_directions)
            if retcode == 1:
                self.vol_path_3d_data["paths"] = {
                    path_id: {
                        "vol_id": vol_id,
                        "scan_x_step": scan_x_step,
                        "scan_y_step": scan_y_step,
                        "scan_z_step": scan_z_step,
                        "path_order": path_order,
                        "path_type": path_type,
                        "path_directions": path_directions
                        }
                }

                self.start_scan.setEnabled(True)
                self.delete_path.setEnabled(True)
                self.path_nid += 1
                self.path_choice.addItem(path_id)
                self.path_choice.setCurrentText(path_id)

    def deletePath(self):
        path_id = self.path_choice.currentText()
        retcode, res = self.pyrame.call("deinit_path@paths",path_id)
        if retcode==1:
            self.path_choice.removeItem(self.path_choice.currentIndex())

            if self.path_choice.count() == 0:
                self.delete_path.setEnabled(False)
                self.start_scan.setEnabled(False)
                
    def reportProgress(self,n):
        self.x_global.setText(f"{n}")
        
    def reportField(self, n):
        p, f = n.split(";")
        self.updatePositionWidget(p)
        self.updateGaussmeterWidget(f)

        # update plot
        self.scan3d_plot.update_plot_data(p,f)

    def scan3d_showProgress(self, i):
        self.scan3d_plot.scan3d_progress.setValue(i)

    def scan3d_finished_scan(self):
        self.scan3d_plot.scan3d_stop.setText("Close")
        self.scan3d_plot.scan3d_suspend.setEnabled(False)

    def scan3D(self):
        if self.thread_started:
            print("========================here=======")
            self.worker.stop()
            self.thread_started = False

        else:
            self.thread_started = True
            self.thread = QThread()

            move_params=[]
            self.worker = MUWorker(move_params,self.pyrame)

            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)

            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

#            self.worker.finished.connect(self.scan3d_finished_scan)
#            self.worker.progress.connect(self.scan3d_showProgress)
            self.worker.field.connect(self.reportField)
            # Step 6: Start the thread
            self.thread.start()


    def scan(self):

        move_params = [self.path_choice.currentText()]
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

        self.worker = MUWorker(move_params,self.pyrame)

        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)

        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.finished.connect(self.scan3d_finished_scan)
        self.worker.progress.connect(self.scan3d_showProgress)
        self.worker.field.connect(self.reportField)
        # Step 6: Start the thread
        self.thread.start()

        self.scan3d_plot = Scan3dPlotDialog(self.worker)
        data_structure = [_Nx, _Xi, _Xf, _Ny, _Yi, _Yf, _Nz, _Zi, _Zf]
        self.scan3d_plot.init_plot_data(data_structure)
        self.scan3d_plot.show()
        self.thread.start()



                
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
