from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from Databank import DB
import MessageBox

class WidgetEstoque(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/estoque.ui', self)
        self.msg = MessageBox.Msg()
        self.db = DB()
        self.dialog = uic.loadUi('ui/dialog_produtos.ui')
        self.set_signals()
        self.listar_produtos()
    
    def set_signals(self):
        self.btn_cadastrar.clicked.connect(lambda: self.dialog.show())
        self.dialog.cadastrar.clicked.connect(lambda: self.cadastrar_produto())

        self.dialog.margem.valueChanged.connect(lambda: self.calcular_valor())
        self.dialog.valor.valueChanged.connect(lambda: self.calcular_margem())
        self.dialog.custo.valueChanged.connect(lambda: self.calcular_valor())

    def listar_produtos(self):
        produtos = self.db.read_products()
        self.table.setRowCount(len(produtos))
        for row in range(0, len(produtos)):
            for column in range(0, len(produtos[0])):
                self.table.setItem(row, column, QTableWidgetItem(str(produtos[row][column])))
                
    def cadastrar_produto(self):
        try:
            self.db.create_product (
                self.dialog.codigo.text().strip() if self.dialog.codigo.text() else None,
                self.dialog.nome.text().strip() if self.dialog.nome.text() else None,
                self.dialog.custo.value() if self.dialog.custo.value() else None,
                self.dialog.valor.value() if self.dialog.valor.value() else None,
                self.dialog.margem.value(),
                self.dialog.estoque.value()
            )
        except Exception as error:
            erro = str(error)
            if 'NOT NULL' in erro:
                erro = 'Campo Obrigatorio: <strong>' + erro.split('.')[1] + '</strong>'
            elif 'UNIQUE' in erro:
                erro = f"Esse {erro.split('.')[1]} já foi cadastrado"
            self.msg.error(erro)
        else:
            self.listar_produtos()
            self.clear_dialog()
            self.dialog.close()

    def alterar_produto(self):
        pass
   
    def calcular_margem(self):
        valor = self.dialog.valor.value()
        custo = self.dialog.custo.value()
        if custo:
            margem = (valor-custo)/custo*100
            self.dialog.margem.setValue(margem)

    def calcular_valor(self):
        margem = self.dialog.margem.value()
        custo = self.dialog.custo.value()
        valor = custo + custo*margem/100
        self.dialog.valor.setValue(valor)

    def show_dialog_alterar(self):
        self.dialog.show()

    def clear_dialog(self):
        self.dialog.codigo.clear()
        self.dialog.nome.clear()
        self.dialog.custo.setValue(0)
        self.dialog.valor.setValue(0)
        self.dialog.margem.setValue(0)
        self.dialog.estoque.setValue(0)

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = WidgetEstoque()

    window.show()
    app.exec()

