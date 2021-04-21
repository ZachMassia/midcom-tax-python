import sys

from midcom_tax.midcom import MIDCOM
from midcom_tax.models import TaxModel

from midcom_tax.main_window import MainWindow

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice


class Controller:
    def __init__(self):
        self.midcom = MIDCOM()
        self.app = QApplication([])
        self.window = MainWindow()

        self.setup_tax_table()

    def setup_tax_table(self):
        data = []
        for t in self.midcom.taxes:
            data.append([
                t.id,
                t.label,
                t.tax_type,
                t.tax_rate,
                t.tax_subtotal
            ])

        self.tax_model = TaxModel(self.midcom.taxes)
        self.window.ui.taxTableView.setModel(self.tax_model)


    @staticmethod
    def load_ui_file(filename: str):
        ui_file = QFile(filename)

        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {filename}: {ui_file.errorString()}")
            sys.exit(-1)

        loader = QUiLoader()
        ui = loader.load(ui_file)
        ui_file.close()

        if not ui:
            print(loader.errorString())
            sys.exit(-1)
        else:
            return ui

    def run_app(self):
        self.window.show()
        return self.app.exec_()
