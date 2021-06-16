from PyQt5 import QtWidgets, QtCore, QtPrintSupport, QtGui
from PyQt5.QtGui import QIcon, QPixmap, QTextTableFormat
import xlwt

class Window(QtWidgets.QDialog):
    def setupui(self, form,table7, table8, name):
        self.setWindowTitle(self.tr('Document Printer'))
        self.table7 = table7
        self.table8 = table8
        self.project_name = name
        self.radioButtom_1 = QtWidgets.QRadioButton('لیست لوازم', form)
        self.radioButtom_1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.radioButtom_2 = QtWidgets.QRadioButton('لیست قیمت', form)
        self.radioButtom_2.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.buttonexcel = QtWidgets.QPushButton('export', form)
        self.buttonexcel.clicked.connect(self.to_excel)

        layout = QtWidgets.QGridLayout(form)
        layout.addWidget(self.radioButtom_1, 1, 1)
        layout.addWidget(self.radioButtom_2, 2, 1)
        layout.setSpacing(20)
        layout.addWidget(self.buttonexcel, 3, 0)

        self.buttonexcel.setEnabled(False)

        self.radioButtom_1.toggled.connect(lambda : self.radio_action(1))
        self.radioButtom_2.toggled.connect(lambda: self.radio_action(2))
    def radio_action(self, num):
        self.buttonexcel.setEnabled(True)
        if num == 1:
            self.table =self.table7
            self.header = ["ردیف", "شرح", "سایز", "فشار کاری", "واحد", "تعداد"]
            self.width = [ QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 55)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 250)
                , QtGui.QTextLength(QtGui.QTextLength.FixedLength, 25)]

        elif num == 2:
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
    def to_excel(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', '', ".xls(*.xls)")
        if filename == QtWidgets.QDialog.Accepted:
            wbk = xlwt.Workbook()
            self.sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
            row = 0
            col = 0
            for i in range(self.table.columnCount()):
                for x in range(self.table.rowCount()):
                    try:
                        teext = str(self.table.item(row, col).text())
                        self.sheet.write(row, col, teext)
                        row += 1
                    except AttributeError:
                        row += 1
                row = 0
                col += 1
            wbk.save(filename[0])
