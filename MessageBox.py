from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon


class Msg(QMessageBox):
    def __init__(self):
        super(Msg, self).__init__()
        self.setWindowTitle('Mosaic')
        #icone = QIcon(r'img/icone.ico')
        #self.setWindowIcon(icone)

    def error(self, txt):
        #self.setIcon(QMessageBox.Critical)
        self.setText(txt)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.exec()

    def question(self, txt):
        #self.setIcon(QMessageBox.question)
        self.setText(txt)
        self.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        confirm = self.exec_()
        return True if confirm == QMessageBox.StandardButton.Ok else False

    def info(self, txt):
        #self.setIcon(QMessageBox.Information)
        self.setText(txt)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.exec()


if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    msg = Msg()
    msg.info('123')
