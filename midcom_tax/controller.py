from midcom_tax.main_window import MainWindow
from midcom_tax.midcom import MIDCOM

from PySide6.QtWidgets import QApplication


class Controller:
    def __init__(self):
        self.midcom = MIDCOM()

        self.app = QApplication([])
        self.main_window = MainWindow(controller=self)

    def run_app(self):
        self.main_window.show()
        return self.app.exec_()
