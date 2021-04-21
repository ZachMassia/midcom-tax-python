from PySide6 import QtCore
from PySide6.QtCore import Qt


class TaxModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TaxModel, self).__init__()
        self._data = data
        self.headers = [
            'ID', 'Label', 'Tax Type $/%', 'Rate XX.XXXX', 'Tax Subtotal? Y/N'
        ]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            tax = self._data[index.row()]
            col = index.column()
            if col == 0:
                return str(tax.id)
            elif col == 1:
                return str(tax.label)
            elif col == 2:
                return str(tax.tax_type)
            elif col == 3:
                return str(tax.tax_rate)
            elif col == 4:
                return str(tax.tax_subtotal)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            col = index.column()
            row = index.row()
            if col == 0:
                return False
            elif col == 1:
                # TODO: Trim input to 15 chars
                self._data[row].label = value
            elif col == 2:
                # TODO: Limit input to '$' or '%'
                self._data[row].tax_type = value
            elif col == 3:
                # TODO: Limit input to 6 digits
                self._data[row].tax_rate = value
            elif col == 4:
                # TODO: Limit input to 'Y' or 'N'
                self._data[row].tax_subtotal = value
            return True

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self.headers)

    def flags(self, index):
        # TODO: Find flag to prevent multiple tab inputs in succession from
        #       essentially clearing everything out.
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
