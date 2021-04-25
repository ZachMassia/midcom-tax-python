import sys
import traceback

from os import path

from midcom_tax.midcom import MIDCOM, InvalidTaxFile
from midcom_tax.models import TaxModel, ProductModel

from midcom_tax.main_window import MainWindow

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication, QHeaderView, QFileDialog, QMessageBox


class Controller:
    def __init__(self):
        self.midcom = MIDCOM()
        self.app = QApplication([])
        self.window = MainWindow()

        self.tax_model = TaxModel(self.midcom.taxes)
        self.setup_tax_table()

        self.product_model = ProductModel(self.midcom.products)
        self.setup_product_table()

        self.setup_file_menu()

    def setup_tax_table(self):
        # Setup table
        table = self.window.ui.taxTableView
        table.setModel(self.tax_model)

        # Use monospace font for table contents.
        # TODO: Break these out into one common font for the controller.
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSize(14)
        table.setFont(font)

        # Setup header
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

    def setup_product_table(self):
        # Setup table
        table = self.window.ui.productTableView
        table.setModel(self.product_model)

        # Use monospace font for table contents.
        # TODO: Break these out into one common font for the controller.
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSize(14)
        table.setFont(font)

        # Setup header
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

    def setup_file_menu(self):
        self.window.ui.actionOpen_File.triggered.connect(self.on_action_open_file)
        self.window.ui.actionExport_SD.triggered.connect(self.on_action_export_sd)
        self.window.ui.actionExport_Cybercard.triggered.connect(self.on_action_export_cybercard)

    def on_action_open_file(self):
        filename = QFileDialog.getOpenFileName(
            parent=self.window,
            caption='Select tax file to open ...',
            filter='Tax Files (*.str *.dat)'
        )
        tax_format = path.splitext(filename[0])[1].lower()

        contents = self.load_file(filename[0])

        if tax_format == '.str':
            print(f'Loading {filename[0]} in SD Card format.')
            self.midcom.load_str(contents)

        elif tax_format == '.dat':
            print(f'Loading {filename[0]} in Cybercard format.')
            self.midcom.load_dat(contents)

    def on_action_export_sd(self):
        contents = self.midcom.get_str()
        filename = QFileDialog.getSaveFileName(
            parent=self.window,
            caption='Export Tax File to SD Card Format',
            filter='SD Card Tax File (*.str)'
        )
        print(f'Writing to {filename[0]} in SD format.')
        self.write_file(filename[0], contents)

    def on_action_export_cybercard(self):
        contents = self.midcom.get_dat()
        filename = QFileDialog.getSaveFileName(
            parent=self.window,
            caption='Export Tax File to Cybercard Format',
            filter='SD Card Tax File (*.dat)'
        )
        print(f'Writing to {filename[0]} in Cybercard format.')
        self.write_file(filename[0], contents)

    def except_hook(self, exc_type, exc_value, exc_tb):
        tb = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        self.show_error_msg(repr(exc_value))
        print(tb)

    @staticmethod
    def show_error_msg(msg):
        m = QMessageBox()
        m.setWindowTitle('MIDCOM Tax File Editor - Error')
        m.setText(f'An error occurred:\n{msg}')
        m.setStandardButtons(QMessageBox.Ok)
        m.exec_()

    @staticmethod
    def write_file(filename, contents):
        with open(file=filename, mode='w', newline='') as file:
            file.write(contents)

    @staticmethod
    def load_file(filename):
        with open(file=filename, newline='') as file:
            return file.read()

    def run_app(self):
        sys.excepthook = self.except_hook

        self.window.show()
        return self.app.exec_()
