import sys
from PyQt6.QtWidgets import QApplication
import Main

app = QApplication(sys.argv)

main = Main.MainWindow()

main.showFullScreen()
app.exec()