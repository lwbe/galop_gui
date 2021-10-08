#! coding: utf-8

import sys,time
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator,QValidator
from galop_ui import Ui_MainWindow
import bind_pyrame


class gotoOrigin_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.scan_order = "XYZ"

current_values = {
    "x_global": "0.0",
    "x_local": "0.0",
    "x_origin": "0.0",
    "x_step": "1.0",
    "x_acc": "0.5",
    "x_speed": "0.5",
    "y_global": "0.0",
    "y_local": "0.0",
    "y_origin": "0.0",
    "y_step": "1.0",
    "y_acc": "0.5",
    "y_speed": "0.5",
    "z_global": "0.0",
    "z_local": "0.0",
    "z_origin": "0.0",
    "z_step": "1.0",
    "z_acc": "0.5",
    "z_speed": "0.5",
    "min_extrusion": "0",
    "max_extrusion": "1",
    "scan_x_step": "1",
    "scan_y_step": "1",
    "scan_z_step": "1",
}


class MainWindow(QMainWindow,Ui_MainWindow):
    AXIS_3D = ["x", "y", "z"]
    PATH_ORDER = ["zxy", "zyx", "yxz", "yzx", "xyz", "xzy"]

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.GLOBAL_POS = {"x": 0.0, "y": 0.0, "z": 0.0}

        self.current_values = current_values
        self.initPyrame()
        self.setInitialValues()

        # init widgets
        # see https://snorfalorpagus.net/blog/2014/08/09/validating-user-input-in-pyqt4-using-qvalidator/
        double_validator = QDoubleValidator()
        for i in self.current_values.keys():
            w = getattr(self, i)
            w.setValidator(double_validator)
            w.textChanged.connect(self.check_state)
            w.textChanged.emit(w.text())

        [self.path.addItem(i) for i in self.PATH_ORDER]

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
        self.create_volume.clicked.connect(self.createVolume)
        self.create_path.clicked.connect(self.createPath)
        self.start_scan.clicked.connect(self.scan)


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
        pyrame_modules_list = ["motion","th_apt","bus","serial","gpib","multimeter","ls460","paths"]
        pyrame_modules_init = {
            "motion" : {
                "axis_x": {
                    "init": ["th_apt(model=LTS300,bus=serial(serialnum=45839057))"],
                    "config": ["300","0"]
                },
                "axis_y": {
                    "init": ["th_apt(model=BSC1_LNR50,bus=serial(serialnum=40828799),chan=1)"],
                    "config": ["50","0"]
                },
                "axis_z": {
                    "init": ["th_apt(model=HSLTS300,bus=serial(serialnum=45897070))"],
                    "config": ["300","0"]
                },
            },
            "multimeter": {
                "gaussmeter": {
                    "init": ["ls_460(bus=gpib(bus=serial(vendor=0403,product=6001,timeout=10),dst_addr=12),Bunits=T,Bmode=0,Bfilter=0,nb_channels=3)"],
                    "config": []
                    },
            }
        }

        for module_name in pyrame_modules_init.keys():
            module_port = bindpyrame.get_port(module_name)



        # extract the ports

        # call Pyrame to init and configure
        pass

    def deinitPyrameModules(self):
        # we inval and deinit the modules
        pass

    def callPyrame(self, pyrame_func, *args):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        function, module = pyrame_func.split("@")
        retcode, res = bindpyrame.sendcmd("localhost",
                              self.module_port[module],
                              "%s_%s" % (function, module),
                              *args)
        if retcode == 0:
            # we open a pop up because of error
            pass
        QApplication.restoreOverrideCursor()
        return retcode, res

    def loadScanParam(self):
        name = QFileDialog.getOpenFileName(self,"Load scan file")

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
            # finally close the code.
            self.close()

        self.deinitPyrameModules()


    def setInitialValues(self):

        # we only know a position, an origin a step an acc a speed
        for param_name, param_value in current_values.items():
            getattr(self, param_name).setText(param_value)
            if param_name == "x_global":
                self.GLOBAL_POS['x'] = float(param_value)

    def move(self):

        # extract axis and direction from the button name
        axis, direction = self.sender().objectName().split("_")

        step = getattr(self, "%s_step" % axis).text()
        acc = getattr(self, "%s_acc" % axis).text()
        speed = getattr(self, "%s_speed" % axis).text()

        retcode, res = self.callPyrame("joystick_gaussbench", axis, direction, step, acc, speed)

        if retcode == 1:
            for a, g in zip(self.AXIS_3D, res.split(",")):
                getattr(self, "%s_global" % a).setText(g)
                o = float(getattr(self, "%s_origin" % a).text())
                getattr(self, "%s_local" % a).setText(str(float(g)-o))

    def setOrigin(self):
        for axis in self.AXIS_3D:
            g = getattr(self, "%s_global" % axis).text()
            getattr(self, "%s_origin" % axis).setText(g)
            getattr(self, "%s_local" % axis).setText("0.")

    def gotoOrigin(self):
        dlg = gotoOrigin_Dialog()
        if dlg.exec_():
            print("Done", dlg.scan_order)
            for a in dlg.scan_order:
                getattr(self, "%s_global" % a).setText(getattr(self, "%s_origin" % a).text())

    def homing(self):
        pass

    def addCurrentPosition(self):
        # set the local position in the points_3D widget

        coord = ",".join([getattr(self, "%s_local" % axis).text() for axis in self.AXIS_3D])

        if not self.points_3d.findItems(coord, Qt.MatchExactly):
            self.points_3d.addItem(coord)



    def deletePosition(self):
        for i in self.points_3d.selectedItems():
            self.points_3d.takeItem(self.points_3d.row(i))


    def createVolume(self):
        print(self.extrusion_axis.currentText())

    def createPath(self):
        pass

    def scan(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
