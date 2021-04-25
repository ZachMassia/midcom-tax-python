import typing

from PySide6 import QtCore
from PySide6.QtCore import Qt


class TaxModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TaxModel, self).__init__()
        self._data = data
        self.headers = [
            'ID',
            'Tax Type "$" / "%"',
            'Rate "XX.XXXX"',
            'Tax Subtotal? "Y" / "N"',
            'Label (15 Character Maximum)'
        ]

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            tax = self._data[index.row()]
            col = index.column()
            if col == 0:
                return str(tax.id)
            elif col == 1:
                return str(tax.tax_type)
            elif col == 2:
                return str(tax.tax_rate)
            elif col == 3:
                return str(tax.tax_subtotal)
            elif col == 4:
                return str(tax.label)

    def setData(self, index: QtCore.QModelIndex, value: typing.Any, role: int = ...):
        if role == Qt.EditRole:
            col = index.column()
            row = index.row()

            # ID
            if col == 0:
                return False

            # Tax Type
            elif col == 1:
                if value not in ['$', '%']:
                    return False
                self._data[row].tax_type = value

            # Tax Rate
            elif col == 2:
                if len(value) != 6:
                    return False
                self._data[row].tax_rate = value

            # Tax Subtotal
            elif col == 3:
                if value not in ['Y', 'N']:
                    return False
                self._data[row].tax_subtotal = value

            # Label
            elif col == 4:
                trimmed = value[:15]
                label_len = len(trimmed)
                if label_len < 15:
                    trimmed += ' ' * (15-label_len)
                print(len(trimmed))
                self._data[row].label = trimmed

            return True

    def rowCount(self, parent: QtCore.QModelIndex = ...):
        return len(self._data)

    def columnCount(self, parent: QtCore.QModelIndex = ...):
        return len(self.headers)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if index.row() == 0:
            # First tax entry cannot be used.
            return Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]


class ProductModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(ProductModel, self).__init__()
        self._data = data
        self.headers = [

        ]

    def data(self, index: QtCore.QModelIndex, role: int = ...) -> typing.Any:
        pass

    def setData(self, index: QtCore.QModelIndex, value: typing.Any, role: int = ...) -> bool:
        pass

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        pass

    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        pass

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        pass

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        pass
