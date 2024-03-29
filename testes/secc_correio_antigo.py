
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import pandas as pd
import sys, os

class PandasModel(QtCore.QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df.copy()

    def toDataFrame(self):
        return self._df.copy()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


def btnAbrir(self):
    options = QtWidgets.QFileDialog.Options()
    options = QtWidgets.QFileDialog.DontUseNativeDialog
    fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Selecione o arquivo log do SECC", os.getcwd(), "csv (*.csv)")
    if fileName:
        win.lineEdit.setText(fileName.replace("/", "\\"))
        
def btnCarregar(self):
    fileName = win.lineEdit.text()
    if fileName:
        df = pd.read_csv(fileName, sep=';', engine='python')
        model = PandasModel(df)
        win.tableView.setModel(model)

app = QtWidgets.QApplication([])
win = uic.loadUi(".\\src\\tela_inicial.ui")
win.pushButton_2.clicked.connect(btnAbrir)
win.pushButton.clicked.connect(btnCarregar)
win.pushButton_4.clicked.connect(app.instance().quit)
win.actionSair.setStatusTip('Encerrar programa')
win.actionSair.triggered.connect(app.quit)

win.show()
sys.exit(app.exec())

