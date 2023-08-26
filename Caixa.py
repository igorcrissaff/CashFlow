from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from Databank import DB

class Caixa(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB()
        uic.loadUi('ui/caixa.ui', self)
        self.dialog = uic.loadUi('ui/dialog_search.ui')
        self.set_signals()

    def set_signals(self):
        self.codigo.returnPressed.connect(lambda: self.toggle_codigo())

    def toggle_codigo(self):
        if not self.codigo.text():
            self.buscar_produtos()
        else:
            print(self.codigo.text().strip())

    def buscar_produtos(self):
        self.dialog.list.clear()
        produtos = self.db.read_products()
        for produto in produtos:
            self.dialog.list.addItem(produto[1])
        self.dialog.show()

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = Caixa()

    window.showMaximized()
    app.exec()