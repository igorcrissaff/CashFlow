from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QFileDialog, QHeaderView, QMenu
from Databank import DB
import MessageBox

class WidgetEstoque(QWidget):
    #funções de configuração
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/estoque.ui', self)
        self.msg = MessageBox.Msg()
        self.db = DB()
        self.dialog = uic.loadUi('ui/dialog_produtos.ui')
        self.table.installEventFilter(self)
        self.set_signals()
        self.listar_produtos()

        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        self.function_flag = 0
    
    def set_signals(self):
        self.btn_cadastrar.clicked.connect(lambda: self.show_dialog_cadastrar())
        self.filtro.textChanged.connect(lambda: self.listar_produtos())
        
        self.dialog.button.clicked.connect(lambda: self.toggle_function())

        self.dialog.margem.valueChanged.connect(lambda: self.calcular_valor())
        self.dialog.valor.valueChanged.connect(lambda: self.calcular_margem())
        self.dialog.custo.valueChanged.connect(lambda: self.calcular_valor())

        self.export_2.clicked.connect(lambda: self.exportar_excel())
        
    def eventFilter(self, source, event):
        if source == self.table and event.type() == event.Type.ContextMenu:
            menu = QMenu()
            update = menu.addAction('Editar')
            delete = menu.addAction('Deletar')

            action = menu.exec(event.globalPos())
            if action == update:
                self.show_dialog_alterar()
            if action == delete:
               self.deletar_produto()

        return super().eventFilter(source, event)
    
    #funções essenciais
    def listar_produtos(self):
        filtro = self.filtro.text().strip()
        produtos = self.db.read_products(filtro=filtro)
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
        codigo = self.dialog.codigo.text()
        produto = {}
        if self.dialog.nome.text():
            produto['nome'] = self.dialog.nome.text().strip()
        if self.dialog.custo.value():
            produto['custo'] = self.dialog.custo.value()
        if self.dialog.valor.value():
            produto['valor'] = self.dialog.valor.value()
        if self.dialog.margem.value():
            produto['margem'] = self.dialog.margem.value()
        try:
            self.db.update_protuct(codigo, produto)
        except Exception as erro:
            self.msg.error(str(erro))
        else:
            self.listar_produtos()
            self.dialog.close()
   
    def deletar_produto(self):
        row = self.table.currentRow()
        ok = self.msg.question(f"Deletar produto: <strong>{self.table.item(row, 1).text()}</strong>")
        if ok:
            codigo = self.table.item(row, 0).text()
            self.db.delete_product(codigo)
            self.listar_produtos()
        
    def exportar_excel(self):
        from pandas import read_sql_query
        tabela = read_sql_query('SELECT * FROM produtos', self.db.connection)
        directory = QFileDialog().getExistingDirectory()
        if directory:
            directory += '/estoque.xlsx'
            tabela.to_excel(directory, index=False)

    def toggle_function(self):
        if self.function_flag == 0:
            self.cadastrar_produto()
        elif self.function_flag == 1:
            self.alterar_produto()

    #funções extras
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

    def clear_dialog(self):
        self.dialog.codigo.clear()
        self.dialog.nome.clear()
        self.dialog.valor.setValue(0)
        self.dialog.custo.setValue(0)
        self.dialog.margem.setValue(0)

    def show_dialog_cadastrar(self):
        self.clear_dialog()
        self.dialog.codigo.setReadOnly(False)
        self.dialog.button.setText('Cadastrar')
        self.dialog.show()
        self.function_flag = 0

    def show_dialog_alterar(self):
        self.dialog.codigo.setReadOnly(True)
        self.dialog.estoque.setReadOnly(True)
        self.dialog.button.setText('Alterar')
        row = self.table.currentRow()
        self.dialog.codigo.setText(self.table.item(row, 0).text())
        self.dialog.nome.setText(self.table.item(row, 1).text())
        self.dialog.custo.setValue(float(self.table.item(row, 2).text()))
        self.dialog.valor.setValue(float(self.table.item(row, 3).text()))
        self.dialog.margem.setValue(float(self.table.item(row, 4).text()))
        self.dialog.estoque.setValue(int(self.table.item(row, 5).text()))
        self.dialog.show()
        self.function_flag = 1
    

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = WidgetEstoque()

    window.show()
    app.exec()

