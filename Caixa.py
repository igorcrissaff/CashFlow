from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from datetime import datetime
from Databank import DB
from MessageBox import Msg

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB()
        uic.loadUi('ui/caixa.ui', self)
        self.dialog = uic.loadUi('ui/dialog_search.ui')
        self.msg = Msg()

        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.set_signals()

    def set_signals(self):
        self.codigo.returnPressed.connect(lambda: self.toggle_codigo())
        self.btn_f1.clicked.connect(lambda: self.finalizar_venda())
        self.btn_f2.clicked.connect(lambda: self.remover_produto())
        self.btn_f3.clicked.connect(lambda: self.cancelar_venda())

        self.dialog.filtro.textChanged.connect(lambda: self.filtrar_produtos())
        self.dialog.table.cellDoubleClicked.connect(lambda: self.select_produto())
        self.dialog.btn.clicked.connect(lambda: self.select_produto())

    def keyPressEvent(self, event) -> None:
        key = event.key()

        if key == Qt.Key.Key_F1:
            self.finalizar_venda()
        if key == Qt.Key.Key_F2:
            self.remover_produto()
        if key == Qt.Key.Key_F3:
            self.cancelar_venda()

        return super().keyPressEvent(event)


    def toggle_codigo(self):
        if not self.codigo.text():
            self.buscar_produtos()
        else:
            self.add_produto()
            self.codigo.clear()

    def filtrar_produtos(self):
        filtro = self.dialog.filtro.text().strip()
        produtos = self.db.read_products('codigo, nome, valor', filtro)
        self.dialog.table.setRowCount(len(produtos))
        for row, produto in enumerate(produtos):
            for column, item in enumerate(produto):
                self.dialog.table.setItem(row, column, QTableWidgetItem(str(item)))

    def buscar_produtos(self):
        self.dialog.table.clearContents()
        produtos = self.db.read_products(campos='codigo, nome, valor')
        self.dialog.table.setRowCount(len(produtos))
        for row, produto in enumerate(produtos):
            for column, item in enumerate(produto):
                self.dialog.table.setItem(row, column, QTableWidgetItem(str(item)))
        self.dialog.show()
    
    def select_produto(self):
        row = self.dialog.table.currentRow()
        if row != -1:
            codigo = self.dialog.table.item(row, 0).text()
            self.codigo.setText(str(codigo))
            self.dialog.close()

    def add_produto(self):
        codigo = self.codigo.text().strip()
        quantidade = self.quantidade.value()
        produto = self.db.consultar_produto(codigo)
        if produto:
            row = self.table.rowCount()
            self.table.setRowCount(row+1)
            self.table.setItem(row, 0, QTableWidgetItem(str(produto[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(produto[1])))
            self.table.setItem(row, 2, QTableWidgetItem(f"R$ {produto[3]:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"X {quantidade}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"R$ {produto[3]*quantidade:.2f}"))

            self.valor.setValue(produto[3])

            self.sub_total.setValue(produto[3]*quantidade)

            total = self.total.value()
            self.total.setValue(total+produto[3]*quantidade)

            self.produto.setText(f"{quantidade} X {produto[1]}")
        else:
            self.msg.error('Produto não cadastrado')

    def finalizar_venda(self):
        if self.table.rowCount() > 0:
            if self.msg.question('Finalizar venda?'):
                data = datetime.now().strftime(r"%Y-%m-%d")
                rows = self.table.rowCount()
                for r in  range(0, rows):
                    produto = [
                        int(self.table.item(r, 0).text()),
                        float(self.table.item(r, 3).text().replace('X', '')),
                        float(self.table.item(r, 4).text().replace('R$', '')),
                        data
                    ]
                    self.db.cadastrar_venda(produto)
                self.table.setRowCount(0)
                self.produto.setText('Caixa Livre')
                self.valor.setValue(0)
                self.sub_total.setValue(0)
                self.total.setValue(0)

    def remover_produto(self):
        row = self.table.currentRow()
        if row == -1:
            self.msg.error('Nenhum produto selecionado')
        else:
            produto = self.table.item(row, 1).text()
            ok = self.msg.question(f"Remover produto: {produto}?")
            if ok:
                valor = float(self.table.item(row, 4).text().replace('R$', ''))
                total = self.total.value()
                self.total.setValue(total-valor)
                self.valor.setValue(0)
                self.sub_total.setValue(0)
                self.produto.setText('')
                self.table.removeRow(row)
            
    def cancelar_venda(self):
        if self.table.rowCount() > 0:
            if self.msg.question('Cancelar venda?'):
                self.table.setRowCount(0)
                self.valor.setValue(0)
                self.sub_total.setValue(0)
                self.total.setValue(0)
                self.produto.setText('Caixa Livre')


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    caixa = Window()

    caixa.showMaximized()
    app.exec()