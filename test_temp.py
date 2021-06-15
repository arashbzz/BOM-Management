from PyQt5 import QtWidgets, QtCore, QtPrintSupport, QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QLabel,
    QVBoxLayout,
    QFileDialog
)
from PyQt5.QtGui import QIcon, QPixmap,QTextTableFormat
import sys

name = "پروژه زیبا"
class Window(QtWidgets.QDialog):
    def setupui(self,form,name):
        self.setWindowTitle(self.tr('Document Printer'))

        self.table = QtWidgets.QTableWidget()
        self.table.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.table.setObjectName("tableWidget")
        self.table.setColumnCount(8)
        self.table.setRowCount(150)
        self.table.setHorizontalHeaderLabels(
            ["ID", "شرح", "سایز", "فشار کاری", "تعداد", ",واحد", "قیمت", "قیمت کل"])

        for row in range(0,150):
            for col in range(0,8):
                self.table.setItem(row, col, QTableWidgetItem(str(col)+ "," + str(row)))
                col += 1
            row += 1
        self.project_name = name
        self.buttonPrint = QtWidgets.QPushButton('Print', form)
        self.buttonPrint.clicked.connect(self.handlePrint)
        self.buttonPreview = QtWidgets.QPushButton('Preview', form)
        self.buttonPreview.clicked.connect(self.handlePreview)
        layout = QtWidgets.QGridLayout(form)
        # layout.addWidget(self.table, 0, 0, 1, 2)
        layout.addWidget(self.buttonPrint, 1, 0)
        layout.addWidget(self.buttonPreview, 1, 1)
        self.handlePreview()
        
    def handlePrint(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePreview(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
        document = QtGui.QTextDocument()
        font = QtGui.QFont("B Nazanin", 20, QtGui.QFont.Bold)
        document.setDefaultFont(font)
        idx = "لیست قیمت اقلام طرح" + " " + self.project_name
        # document.setDocumentMargin(10)

        document.setPlainText(str(idx))

        cursor = QtGui.QTextCursor(document)
        cursor.movePosition(QtGui.QTextCursor.End)
        font = QtGui.QFont("B Nazanin", 12)
        # document.setDefaultFont(font)

        fmt = QtGui.QTextTableFormat()
        fmt.setAlignment(QtCore.Qt.AlignHCenter)
        width = [QtGui.QTextLength(QtGui.QTextLength.FixedLength, 125)
            , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 100)
            , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
            , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
            , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
            , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 55)
            , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 250)
            , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)]

        fmt.setCellSpacing(False)
        fmt.setCellPadding(False)
        fmt.setColumnWidthConstraints(width)
        fmt.setHeaderRowCount(1)
        # fmt.setWidth(QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 100))
        fmt.setBorderStyle(QtGui.QTextFrameFormat.BorderStyle_Solid)

        table = cursor.insertTable(self.table.rowCount() + 1, self.table.columnCount(), fmt)

        # fmt = table.format()

        # table.setFormat(fmt)

        format1 = cursor.blockCharFormat()
        # format.setFontWeight(QtGui.QFont.Bold)
        # format.setLayoutDirection(QtCore.Qt.RightToLeft)
        format1.setFont(font)
        # format.setVerticalAlignment(QtGui.QTextCharFormat.AlignMiddle)
        # format1.setVerticalAlignment(QtGui.QTextCharFormat.VerticalAlignment)

        format = cursor.blockFormat()
        format.setAlignment(QtCore.Qt.AlignHCenter)

        # format.setAlignment(QtCore.Qt.AlignVCenter)

        header = ["ردیف", "شرح", "سایز", "فشار کاری", "واحد", "تعداد", "قیمت", "قیمت کل"]
        for item in reversed(header):
            cursor.setBlockCharFormat(format1)
            cursor.setBlockFormat(format)
            cursor.insertText(item)
            cursor.movePosition(QtGui.QTextCursor.NextCell)
        r = 1
        txt = "*"
        for row in range(table.rows() - 1):
            for col in range(7, -1, -1):
                # w = self.tableWidget8.cellWidget(row, col+1)

                if col == 0:
                    txt = str(r)
                    r += 1
                elif row == self.table.rowCount() and self.check == 2 :
                    txt=""
                else:
                    it = self.table.item(row, col)
                    if it is not None:
                        txt = it.text()
                cursor.setBlockCharFormat(format1)
                cursor.setBlockFormat(format)
                cursor.insertText(txt)
                cursor.movePosition(QtGui.QTextCursor.NextCell)
        table.mergeCells(self.table.rowCount() , 1, self.table.rowCount() , 7)
        table.cellAt(self.table.rowCount() , self.table.rowCount())


        print(self.table.item(self.table.rowCount()-1, 7).text())
        cursor.movePosition(QtGui.QTextCursor.StartOfBlock)

        cursor.movePosition(QtGui.QTextCursor.EndOfBlock)
        cursor.selectionEnd()
        cursor.insertText("dmflksdmldskmldfk")

        document.print_(printer)

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QDialog()
ui = Window()
ui.setupui(MainWindow,name)
MainWindow.show()
sys.exit(app.exec_())