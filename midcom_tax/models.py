import typing

from midcom_tax.midcom import Product

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
            'ID',
            'Product tax combination'
        ]

    def data(self, index: QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            product = self._data[index.row()]
            col = index.column()
            if col == 0:
                return str(product.id)
            elif col == 1:
                xs = []
                for x in product.taxes:
                    if x == '00' and len(xs) == 0:
                        xs = ['00']
                        break
                    elif x == '00':
                        break
                    xs.append(x)
                return ''.join(xs)

    def setData(self, index: QtCore.QModelIndex, value: typing.Any, role: int) -> bool:
        if role == Qt.EditRole:
            col = index.column()
            row = index.row()

            # ID
            if col == 0:
                return False

            # Product Code
            elif col == 1:
                self._data[row].load_user_input_str(value)

            return True

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return len(self.headers)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if index.row() == 0:
            return Qt.ItemIsSelectable
        elif index.column() == 0:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
