#! coding: utf-8

import sys,time
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QDialogButtonBox, QVBoxLayout, QLabel,QMessageBox
from PySide6.QtCore import QThread, QObject, Signal
from galop_ui import Ui_MainWindow

current_values = {
    "x":
        {
            "global": "0.0",
            "local": "0.0",
            "step": "1.0",
            "acc": "0.5",
            "speed": "0.5"
        },
    "y":
        {
            "global": "0.0",
            "local": "0.0",
            "step": "1.0",
            "acc": "0.5",
            "speed": "0.5"
        },
    "z":
        {
            "global": "0.0",
            "local": "0.0",
            "step": "1.0",
            "acc": "0.5",
            "speed": "0.5"
        }
}


class PyrameWorker(QObject):
    finished = Signal()
    progress = Signal(int)

    def __init__(self, connected_widget=None):
        super().__init__()
        self.widget = connected_widget
        print('called')

    def run(self):
        """Call Pyrame code"""
        #for i in range(5):
        #    print(i)
        #    sleep(1)
            #self.progress.emit(i + 1)
        #self.connected_widget.close()
        print("let emit something")
        self.finished.emit()


class CustomDialog(QDialog):
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

class AutoCloseDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Information")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.current_values = current_values
        self.setCurrentValues()


        # connect
        self.x_m.clicked.connect(self.move("x", "m"))
        self.x_p.clicked.connect(self.move("x", "p"))
        self.y_m.clicked.connect(self.move("y", "m"))
        self.y_p.clicked.connect(self.move("y", "p"))
        self.z_m.clicked.connect(self.move("z", "m"))
        self.z_p.clicked.connect(self.move("z", "p"))


    def setCurrentValues(self):
        for axis, values in current_values.items():
            for param_name, param_value in values.items():
                getattr(self, "%s_%s" % (axis, param_name)).setText(param_value)

    def closedlg(self):
        time.sleep(10)
        print(" closedlg")
        self.dlg.close()


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



            self.dlg = AutoCloseDialog(self)
            #print(" start time")
            #self.timer = QTimer()
            #self.timer.setSingleShot(True)
            #self.timer.setInterval(0)
            #self.timer.timeout.connect(self.closedlg)
            #self.timer.start(10)



            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = PyrameWorker(self.dlg)
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            #self.worker.progress.connect(self.reportProgress)
            # Step 6: Start the thread
            self.thread.start()


            print("start dialog")
            if self.dlg.exec():
                print("Success!")
            else:
                print("Cancel!")


            # call pyrame move
            retcode,res = 0,1.0
            s = float(step)
            if dir == "m":
                s*= -1

            self.current_values[axis]["global"] = str(float(self.current_values[axis]["global"]) + s)
            self.current_values[axis]["local"] = str(float(self.current_values[axis]["local"]) + s)

            # update the value in the interface
            print(dir, axis,step,acc,speed,self.current_values[axis]["global"])
            self.setCurrentValues()

        return f





if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
