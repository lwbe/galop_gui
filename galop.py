#! coding: utf-8

import sys,time
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout, QHBoxLayout,QGridLayout,
    QLabel,
    QMessageBox,
    QFileDialog,
    QLineEdit,
    QComboBox
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator,QValidator
from galop_ui import Ui_MainWindow
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
    "multimeter": {
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


# Custom widget
class orderedMovement_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ordered move")

        self.explanation = QLabel('')

        orderLabel = QLabel("&Order")
        self.orderCombo = QComboBox()
        orderLabel.setBuddy(self.orderCombo)
        self.orderCombo.currentTextChanged.connect(self.onChanged)

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

        self.scan_order = ""

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
            self.setLayout(self.layout)


# The main class
class MainWindow(QMainWindow,Ui_MainWindow):
    AXIS_3D = ["x", "y", "z"]
    PATH_ORDER = ["zxy", "zyx", "yxz", "yzx", "xyz", "xzy"]

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.volume_nid = 0
        self.initPyrameModules()
        self.coords_3d_scan = []
        self.setInitialValues()

        # setting QDoubleValidator for all QLineEdit widgets
        # beware QDoubleValidator depend on locale
        # see https://snorfalorpagus.net/blog/2014/08/09/validating-user-input-in-pyqt4-using-qvalidator/
        double_validator = QDoubleValidator()
        for i in self.findChildren(QLineEdit):
            w = getattr(self, i.objectName())
            w.setValidator(double_validator)
            #w.setText("1.0")
            w.textChanged.connect(self.check_state)
            w.textChanged.emit(w.text())

        # add some value to path widget
        [self.path.addItem(i) for i in self.PATH_ORDER]
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
        self.create_path.clicked.connect(self.createPath)
        self.create_path.setEnabled(False)
        self.start_scan.clicked.connect(self.scan)
        self.start_scan.setEnabled(False)

        self.extrusion_axis.addItems(reversed(self.AXIS_3D))
        
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

    # Pyrame Stuff
    def initPyrameModules(self):
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
                        retcode, res = self.callPyrame(
                            "%s@%s" % (function,module),
                            uid,
                            *params[function]
                        )

    def deinitPyrameModules(self):
        # we inval and deinit the modules
        for module, values in self.pyrame_modules_init.items():
            for uid, params in values.items():
                order = params.get('deinit_order', ["inval","deinit"])
                for function in order:
                         retcode, res = self.callPyrame(
                             "%s@%s" % (function, module),
                             uid
                         )

    def callPyrame(self, pyrame_func, *args):
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
                self,
                "Error in callPyrame",
                "%s" % res,
                buttons=QMessageBox.Ok)
        QApplication.restoreOverrideCursor()
        return retcode, res

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
            self.deinitPyrameModules()
            self.close()

    def updatePositionWidget(self):
        retcode, res = self.callPyrame("get_position@paths","space_1")
        if retcode == 1:
            p = res.split(',')
            print(p)
            for a, c in zip(self.AXIS_3D, p):
                w = getattr(self, "%s_global" % a )
                w.setText(c)
                w = getattr(self, "%s_origin" % a)
                o = float(w.text())
                w = getattr(self, "%s_local" % a)
                w.setText(str(float(c) - o))

    def setInitialValues(self):
        """
        init interface with value in a conf file or internal data and by querying the devices
        :return:
        """
        for w, v in initial_values.items():
            getattr(self, w).setText(v)

        self.updatePositionWidget()

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
        retcode, res = self.callPyrame("move_space@paths","space_1",*(pos+speed+acc))
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
            if dlg.scan_order:
                for d in dlg.scan_order:          
                    retcode, res = self.callPyrame("home@motion", "axis_%s" % d,"r","1")
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
        for i in range(self.points_3d.count()):
            coords = self.points_3d.item(i).text().split(',')
            new_coords += "%s,%s;" % (float(coords[c0]) + origin[c0],float(coords[c1]) + origin[c1])
            
        coords = self.points_3d.item(0).text().split(',')
        new_coords += "%s,%s;" % (float(coords[c0]) + origin[c0],float(coords[c1]) + origin[c1])

        # we need to ask for a name for the vol_id
        dlg = askForName()
        dlf.message.setText("Enter volume id")
        dlg.linEditField.setText("vol_%d" % self.volume_nid)
        if dlg.exec_():
            vol_id = dlg.lineEditField.text()
            print("""retcode, res = self.callPyrame("init_volume@paths",
                                           vol_id,
                                           "space_1",
                                           "prism",
                                           "prism",
                                           new_coords,
                                           ext_axis,
                                           "%s" % (axis_min+origin[c2]),
                                           "%s" % (axis_max+origin[c2]))"""
            if retcode == 1:
                self.create_path.setEnabled(True)
                self.volume_nid += 1



    def createPath(self):
        pass

    def scan(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
