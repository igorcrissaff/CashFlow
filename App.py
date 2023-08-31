import sys
from PyQt6.QtWidgets import QApplication
import Admin
import Caixa

app = QApplication(sys.argv)

admin = Admin.MainWindow()
caixa = Caixa.Window()

admin.caixa.clicked.connect(lambda: caixa.showMaximized())

admin.showMaximized()
app.exec()