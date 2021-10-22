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

        self.lx = 30
        self.ly = 30
        self.points = np.arange(self.lx*self.ly)


    def run(self):




        for i in self.points:
            if not self._isrunning:
                self.finished.emit()
            elif not self._issuspended:
                #QApplication.processEvents() # to get event from the GUI
                y = int(i/self.lx)
                x = i - y * self.lx
                position = "%d,%d,%d" % (x,y,0.1)
                bx = -np.sin(.10 * ((x/10.)**2 + (y/10)**2)) / 10.
                field = "%f,%f,%f,%f" % (bx,-bx,2*bx,1-bx)
                print("data", position, field)
                self.field.emit("%s;%s" % (position, field))

                self.progress.emit(100.*i/self.points[-1])

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
        self.scan3d_plottype.addItems(["surface","wireframe"])

        self.scan3d_plottype.currentTextChanged.connect(self.update_plot_base)
        self.scan3d_plottype.currentTextChanged.connect(self.update_plot_data_structure)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.is_started = False

        #self.fig.set_canvas(self.canvas)
        self._ax = self.canvas.figure.add_subplot(projection="3d")

        self._ax.set_xlabel("X")
        self._ax.set_ylabel("Y")
        self._ax.set_zlabel("Z")
        #self.plot_wire()
        self._ax.view_init(30, 30)
        self.plot_object=None

    def stop(self):
        self.working_thread.stop()
        self.accept()

    def suspend(self):
        self.working_thread.suspend()
        if self.scan3d_suspend.text() == "suspend":
            self.scan3d_suspend.setText("resume")
        else:
            self.scan3d_suspend.setText("suspend")

    def update_plot_data_structure(self):
        # to be done to set the X Y Z component to plot
        pass

    def init_plot_data(self,lx,ly):
        if not self.is_started:
            self.timer.start(5000)
            self.is_started = True
        x = np.arange(lx)
        y = np.arange(ly)
        self.X,self.Y = np.meshgrid(x,y)
        self.Z=np.zeros(self.X.shape)


    def update_plot_data(self,position,field):
        x,y,z = map(int,position.split(","))
        bx,by,bz,bn = map(float,field.split(","))
        self.Z[x,y]= bx
        print("Field data ",x,y,bx)

    def update_plot(self):
        if self.scan3d_update.isChecked():
            self.update_plot_base()

    def update_plot_base(self):
        print("updating plot base")
        if self.plot_object:
            self._ax.collections.remove(self.plot_object)
        if self.scan3d_plottype.currentText() == "surface":
            self.plot_object = self._ax.plot_surface(self.X, self.Y, self.Z,rstride=1, cstride=1, cmap="viridis", edgecolor="none")
        elif self.scan3d_plottype.currentText() == "wireframe":
            self.plot_object = self._ax.plot_wireframe(self.X, self.Y, self.Z,rstride=1, cstride=1, cmap="viridis")
        self.canvas.draw()

    def plot_contour(self):
        cset = self._ax.contour(self.X, self.Y, self.Z, zdir='z', offset=self.Z.min(), cmap=cm.coolwarm)
        cset = self._ax.contour(self.X, self.Y, self.Z, zdir='x', offset=self.X.min(), cmap=cm.coolwarm)
        cset = self._ax.contour(self.X, self.Y, self.Z, zdir='y', offset=self.Y.min(), cmap=cm.coolwarm)

    def plot_wire(self):
        # Data
        #self.X, self.Y, self.Z = axes3d.get_test_data(0.03)
        x = np.arange(-30,30)
        y = np.arange(-30,30)
        self.X,self.Y = np.meshgrid(x,y)
        self.Z=np.zeros(self.X.shape)
        for i in range(len(x)):
            for j in range(len(y)):
                self.Z[i,j] = -np.sin(.10 * ((i/10.)**2 + (j/10)**2)) / 10.

        #cset = self._ax.contourf(self.X, self.Y, self.Z, cmap=cm.coolwarm)
        #self._ax.plot_wireframe(self.X, self.Y, self.Z, rstride=10, cstride=10, cmap="viridis")
        self._ax.plot_surface(self.X, self.Y, self.Z,
                              rstride=1, cstride=1, cmap="viridis", edgecolor="none")
        self.plot_contour()
        self.canvas.draw()

    def stop_timer(self):
        self.timer.stop()

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
        name = QFileDialog.getOpenFileName(self, "Load scan file")

    def saveScanParam(self):
        name = QFileDialog.getSaveFileName(self, 'Save scan file')
        if name[0] != "":
            l = np.min([len(self.x), len(self.y), len(self.y1)])
            if l == 0:
                dlg = QMessageBox.about(self, "Save Data", "No data to save")
                return
            file = open(name[0], 'w')
            file.write("# t(s)  P(mbar) Pump on (1) 0 (off)")
            for i in range(l):
                f.write("%e %e %e\n" % (self.x[i], self.y[i], self.y1[i]))
            file.close()

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
                self.vol_path_3d_data[vol_id] = {"origin":origin, "ext_axis":ext_axis, "axis_min":axis_min, "axis_max":axis_max, "all_coords":all_coords}
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
            retcode,res = self.pyrame.call("init_path@paths",path_id,"space_1",vol_id,scan_x_step,scan_y_step,scan_z_step,path_order,"rr","ppp")
            if retcode == 1:
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
        self.scan3d_plot.update_plot_data(p,f)

    def scan3d_showProgress(self, i):
        self.scan3d_plot.scan3d_progress.setValue(i)

    def scan3d_finished_scan(self):
        self.scan3d_plot.scan3d_stop.setText("Close")
        self.scan3d_plot.scan3d_suspend.setEnabled(False)
        self.scan3d_plot.stop_timer()


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
        self.scan3d_plot.init_plot_data(30,30)
        self.scan3d_plot.show()
        self.thread.start()



                
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
