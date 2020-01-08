from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, 
                             QTableView, QHBoxLayout, QVBoxLayout, QGroupBox, QFileDialog, 
                             QMessageBox)
from PyQt5.QtGui import QIcon, QBrush
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex
from os import getcwd
import sys
import pandas as pd

class PandasModel(QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QAbstractTableModel.__init__(self, parent=parent)
        self._df = df.copy()

    def toDataFrame(self):
        return self._df.copy()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role !=Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QVariant()
        elif orientation == Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        elif role == Qt.BackgroundColorRole:
            if str(self._df.ix[index.row(), index.column()]) == '1561944':
                return QBrush(Qt.yellow)
            # else:
            #     return QBrush(Qt.red)
        elif role != Qt.DisplayRole:
            return QVariant()

        return QVariant(str(self._df.ix[index.row(), index.column()]))

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

    def rowCount(self, parent=QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

def btnAbrir(self):
    options = QFileDialog.Options()
    options =QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(None, "Selecione o arquivo log do SECC", getcwd(), "csv (*.csv)")
    if fileName:
        app.caixaArquivo.setText(fileName.replace("/", "\\"))

def btnCarregar(self):
    fileName = app.caixaArquivo.text()
    if fileName:
        df = pd.read_csv(fileName, sep=';', engine='python')
        df = df.rename(columns={df.columns[0]:'Processo', df.columns[1]:'Entidade', df.columns[2]:'CPF/CNPJ', df.columns[3]:'Tipo Doc.', df.columns[4]:'Num. doc. Sigec', df.columns[5]:'Num. Sei', df.columns[15]:'Data', df.columns[18]:'Usuário'})
        df2 = df[['Processo','Entidade', 'CPF/CNPJ', 'Tipo Doc.', 'Num. doc. Sigec', 'Num. Sei', 'Data', 'Usuário']]
        df2['Status']=""
        model = PandasModel(df2)
        app.tabela.setModel(model)

def btnProcessar(self):
    docsei = app.tabela.model().data(app.tabela.model().index(0, 5))
    tam = app.tabela.model().rowCount()
    print (str(tam))
    print (docsei.value())


class Principal(QWidget):
    def __init__(self, parent=None):
        super(Principal, self).__init__()
        self.setWindowTitle("Encaminha Notifiações SECC pelo Módulo SEI Correios")
        self.setWindowIcon(QIcon(".\\src\\app_icone.png"))
        self.resize(900, 400)
        self.grupo = QGroupBox("Selecione o arquivo contendo a lista de documentos gerados no SECC (*.csv):")
        self.botaoAbrir = QPushButton("Abrir")
        self.botaoCarregar = QPushButton("Carregar")
        self.botaoSair = QPushButton("Sair")
        self.botaoProcessar = QPushButton("Processar")
        self.caixaArquivo = QLineEdit()
        self.tabela = QTableView()
        self.layout_selecao = QHBoxLayout()
        self.layout_selecao.addWidget(self.caixaArquivo)
        self.layout_selecao.addWidget(self.botaoAbrir)
        self.layout_selecao.addWidget(self.botaoCarregar)
        self.grupo.setLayout(self.layout_selecao)
        self.layout_inferior = QHBoxLayout()
        self.layout_inferior.addWidget(self.botaoProcessar)
        self.layout_inferior.addWidget(self.botaoSair)
        self.layout_principal = QVBoxLayout()
        self.layout_principal.addWidget(self.grupo)
        self.layout_principal.addWidget(self.tabela)
        self.layout_principal.addLayout(self.layout_inferior)
        self.setLayout(self.layout_principal)
        self.botaoAbrir.clicked.connect(btnAbrir)
        self.botaoCarregar.clicked.connect(btnCarregar)
        self.botaoSair.clicked.connect(root.instance().quit)
        self.botaoProcessar.clicked.connect(btnProcessar)

root=QApplication(sys.argv)
app = Principal()
app.show()
sys.exit(root.exec_())
