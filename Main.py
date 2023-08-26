from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
import Estoque

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/admin.ui', self)
        self.sections()
        self.set_signals()

    def set_signals(self):
        self.exit.clicked.connect(lambda: self.close())
        self.minimize.clicked.connect(lambda: self.showMinimized())

        self.btn_estoque.clicked.connect(lambda: self.body.setCurrentWidget(self.estoque))

    def sections(self):
        self.estoque = Estoque.WidgetEstoque()
        self.body.addWidget(self.estoque)

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()

    window.showFullScreen()
    app.exec()