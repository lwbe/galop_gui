#! coding: utf-8

import sys,time
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QDialogButtonBox, QVBoxLayout, QLabel,QMessageBox
from PySide6.QtCore import Qt, QObject, Signal
from galop_ui import Ui_MainWindow

current_values = {
    "x":
        {
            "global": "0.0",
            "local": "0.0",
            "origin": "0.0",
            "step": "1.0",
            "acc": "0.5",
            "speed": "0.5"
        },
    "y":
        {
            "global": "0.0",
            "local": "0.0",
            "origin": "0.0",
            "step": "1.0",
            "acc": "0.5",
            "speed": "0.5"
        },
    "z":
        {
            "global": "0.0",
            "local": "0.0",
            "origin": "0.0",
            "step": "1.0",
            "acc": "0.5",
            "speed": "0.5"
        }
}


class MainWindow(QMainWindow,Ui_MainWindow):
    AXIS_3D = ["x", "y", "z"]

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.current_values = current_values
        self.setCurrentValues()

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

    def callPyrame(self,pyrame_func,*args):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        time.sleep(10)
        if pyrame_func == "set_origin_gaussbench":
            val = "0.5,0.5,0.5"
        else:
            val = "1.0,2.0,3.0;1.0,2.0,3.0"

        QApplication.restoreOverrideCursor()
        return 1, val

    def setCurrentValues(self):
        for axis, values in current_values.items():
            for param_name, param_value in values.items():
                getattr(self, "%s_%s" % (axis, param_name)).setText(param_value)

    def move(self, axis, dir):
        """
        create move function
        :param dir:
        :param axis:
        :return:
        """
        def f():
            # get the params
            step = getattr(self, "%s_step" % axis).text()
            acc = getattr(self, "%s_acc" % axis).text()
            speed = getattr(self, "%s_speed" % axis).text()

            # call pyrame move
            retcode,res = self.callPyrame("joystick_gaussbench", axis, dir, step,
                                            speed, speed, speed,
                                            acc,acc, acc)
            if retcode == 1:
                local_p, global_p = res.split(";")
                for a, l, g in zip(self.AXIS_3D, local_p.split(","), global_p.split(",")):
                    self.current_values[a]["local"] = l
                    self.current_values[a]["global"] = g

            # update the value in the interface
            self.setCurrentValues()

        return f

    def setOrigin(self):
        retcode, res = self.callPyrame("define_origin_gaussbench")
        if retcode == 1:
            for a, p in zip(self.AXIS_3D, res.split(",")):
                    self.current_values[a]["origin"] = p

        self.setCurrentValues()

    def gotoOrigin(self):
        pass

    def homing(self):
        pass

    def addCurrentPosition(self):
        pass

    def deletePosition(self):
        pass

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
