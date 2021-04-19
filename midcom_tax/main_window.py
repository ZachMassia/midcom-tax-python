from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QMainWindow


class Test(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.txt = QtWidgets.QLabel(self.controller.midcom.get_dat())
        self.txt.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.txt)


class MainWindow(QMainWindow):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = controller
        self.test = Test(self.controller)

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('MIDCOM 8000 Tax File Editor')
        self.setCentralWidget(self.test)
