from PyQt5 import QtWidgets, QtCore, QtPrintSupport, QtGui
from PyQt5.QtGui import QIcon, QPixmap, QTextTableFormat


class Window(QtWidgets.QDialog):
    def setupui(self, form,table7, table8, name):
        self.setWindowTitle(self.tr('پرینت'))
        self.table7 = table7
        self.table8 = table8
        self.project_name = name
        self.radioButtom_1 = QtWidgets.QRadioButton('لیست لوازم', form)
        self.radioButtom_1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.radioButtom_2 = QtWidgets.QRadioButton('لیست قیمت', form)
        self.radioButtom_2.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.buttonPrint = QtWidgets.QPushButton('پرینت', form)
        self.buttonPrint.clicked.connect(self.handlePrint)
        self.buttonPreview = QtWidgets.QPushButton('پیش نمایش', form)
        self.buttonPreview.setEnabled(False)

        self.buttonPreview.clicked.connect(self.handlePreview)
        layout = QtWidgets.QGridLayout(form)
        layout.addWidget(self.radioButtom_1, 1, 1)
        layout.addWidget(self.radioButtom_2, 2, 1)
        layout.setSpacing(20)
        layout.addWidget(self.buttonPrint, 3, 0)
        layout.addWidget(self.buttonPreview, 3, 1)
        self.buttonPreview.setEnabled(False)
        self.buttonPrint.setEnabled(False)
        self.radioButtom_1.toggled.connect(lambda : self.radio_action(1))
        self.radioButtom_2.toggled.connect(lambda: self.radio_action(2))

    def radio_action(self, num):
        self.buttonPrint.setEnabled(True)
        self.buttonPreview.setEnabled(True)
        if num == 1:
            self.check = 1
            self.table =self.table7
            self.header = ["ردیف", "شرح", "سایز", "فشار کاری", "واحد", "تعداد"]
            self.width = [ QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 55)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 250)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)]

        elif num == 2:
            self.check = 2
            self.table = self.table8
            self.header = ["ردیف", "شرح", "سایز", "فشار کاری", "واحد", "تعداد", "قیمت", "قیمت کل"]
            self.width = [QtGui.QTextLength(QtGui.QTextLength.FixedLength, 125)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 100)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 55)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 250)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)]

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

        document.setPlainText(str(idx))

        cursor = QtGui.QTextCursor(document)
        cursor.movePosition(QtGui.QTextCursor.End)
        font = QtGui.QFont("B Nazanin", 12)

        fmt = QtGui.QTextTableFormat()
        fmt.setAlignment(QtCore.Qt.AlignHCenter)

        fmt.setCellSpacing(False)
        fmt.setCellPadding(False)
        fmt.setColumnWidthConstraints(self.width)
        fmt.setHeaderRowCount(1)
        fmt.setBorderStyle(QtGui.QTextFrameFormat.BorderStyle_Solid)
        table = cursor.insertTable(self.table.rowCount() + 1, self.table.columnCount(), fmt)

        format1 = cursor.blockCharFormat()
        format1.setFont(font)

        format = cursor.blockFormat()
        format.setAlignment(QtCore.Qt.AlignHCenter)

        for item in reversed(self.header):
            cursor.setBlockCharFormat(format1)
            cursor.setBlockFormat(format)
            cursor.insertText(item)
            cursor.movePosition(QtGui.QTextCursor.NextCell)
        r = 1
        txt = "*"
        for row in range(table.rows() - 1):
            for col in range(self.table.columnCount()-1, -1, -1):

                if row == self.table.rowCount()-1 and self.check == 2 and col in range(0,7):
                    txt=""
                elif col == 0:
                    txt = str(r)
                    r += 1
                elif col in (6,7) and self.check == 2:
                    it = self.table.item(row, col)
                    txt = float(it.text())
                    txt = "{:,.{}f}".format(txt,2)
                else:
                    it = self.table.item(row, col)
                    if it is not None:
                        txt = it.text()
                cursor.setBlockCharFormat(format1)
                cursor.setBlockFormat(format)
                cursor.insertText(txt)
                cursor.movePosition(QtGui.QTextCursor.NextCell)
        if self.check == 2:
            table.mergeCells(self.table.rowCount(), 1, self.table.rowCount(), 7)
            cursor.insertText("مجموع")

        document.print_(printer)
