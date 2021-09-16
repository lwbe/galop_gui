#! coding: utf-8

import sys,time
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator,QValidator
from galop_ui import Ui_MainWindow


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

        self.current_values = current_values
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

        # connect button to function
        self.x_m.clicked.connect(self.move("x", "m"))
        self.x_p.clicked.connect(self.move("x", "p"))
        self.y_m.clicked.connect(self.move("y", "m"))
        self.y_p.clicked.connect(self.move("y", "p"))
        self.z_m.clicked.connect(self.move("z", "m"))
        self.z_p.clicked.connect(self.move("z", "p"))
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

    def callPyrame(self,pyrame_func,*args):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        time.sleep(10)
        if pyrame_func == "set_origin_gaussbench":
            val = "0.5,0.5,0.5"
        else:
            val = "1.0,2.0,3.0;1.0,2.0,3.0"
        QApplication.restoreOverrideCursor()

        retcode, val = 0, "err msg"
        if retcode == 0:
            pass

        return retcode, val

    def setInitialValues(self):
        for param_name, param_value in current_values.items():
            getattr(self, param_name).setText(param_value)

    def move(self, axis, dir):
        """
        create move function
        :param dir:
        :param axis:
        :return:
        """
        def f():
            # get the params from the interface
            step = getattr(self, "%s_step" % axis).text()
            acc = getattr(self, "%s_acc" % axis).text()
            speed = getattr(self, "%s_speed" % axis).text()

            # call pyrame move
            retcode, res = self.callPyrame("joystick_gaussbench", axis, dir,
                                           step, acc, speed)

            if retcode == 1:
                local_p, global_p = res.split(";")
                for a, l, g in zip(self.AXIS_3D, local_p.split(","), global_p.split(",")):
                    self.current_values[a]["global"] = g

            # update the value in the interface
            self.setCurrentValues()

        return f

    def setOrigin(self):
        retcode, res = self.callPyrame("set_origin_gaussbench")
        if retcode == 1:
            for a, p in zip(self.AXIS_3D, res.split(",")):
                self.current_values["%s_origin" % a] = p

        self.setCurrentValues()

    def gotoOrigin(self):
        dlg = gotoOrigin_Dialog()
        if dlg.exec_():
            print("Done", dlg.scan_order)

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
        pass

    def createPath(self):
        pass

    def scan(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
