from PyQt5 import QtWidgets, QtGui, QtCore, QtPrintSupport, Qt
from PyQt5.QtWidgets import*
import sys
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # Main UI code goes here
        self.resize(300,200)
        self.printButton = QtWidgets.QPushButton("Print", self)
        self.printButton.clicked.connect(self.printing)
        self.textbox = QLineEdit(self)
        self.textbox.move(50,100)
        # End Main UI code
        self.show()

    def printing(self):
            printer = QtPrintSupport.QPrinter()
            x = self.textbox.text()
            print(x)
            painter = QtGui.QPainter()
            header = QtGui.QTextDocument("<h1<Header</h1>")
            body = QtGui.QTextDocument("content...")
            footer = QtGui.QTextDocument("Pagenumber")
            dialog = QtPrintSupport.QPrintDialog(printer)
            if dialog.exec_() == QtPrintSupport.QPrintDialog.Accepted:
                painter.begin(printer)
                painter.drawText(10,10,"Hellow my new print check")
                painter.drawText(50,50,self.textbox.text())
                print("What needs to go here???")

                painter.end()


if __name__ == '__main__':  # only run this code if this script is called directly
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle("Printing")
    sys.exit(app.exec())