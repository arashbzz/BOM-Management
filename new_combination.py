import sqlite3
import sys
import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget
)

class combination_managment(QtWidgets.QDialog):
    def setupUi(self, Form):
        font = QtGui.QFont("B Nazanin", 12)
        Form.setFont(font)

        self.connection = sqlite3.connect('equipment _data.db')

        Form.setObjectName("مدیریت مجموعه ها")
        Form.setWindowTitle("مدیریت مجموعه ها")

        Form.resize(700, 500)

        self.cancelButton = QtWidgets.QPushButton(Form)
        self.cancelButton.setText("خروج")
        self.cancelButton.clicked.connect(lambda: self.close())

        self.newButton = QtWidgets.QPushButton(Form)
        self.newButton.setText("مجموعه جدید")
        self.newButton.clicked.connect(self.new_combination_box)

        self.editButton = QtWidgets.QPushButton(Form)
        self.editButton.setText("اصلاح مجموعه")
        self.editButton.clicked.connect(self.edit_combination_box)

        self.comboList = QtWidgets.QComboBox(Form)
        self.comboList.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.comboList.currentIndexChanged.connect(self.load_data)

        self.tableWidget1 = QtWidgets.QTableWidget(Form)
        self.tableWidget1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget1.setObjectName("tableWidget")
        self.tableWidget1.setColumnCount(5)
        self.tableWidget1.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری", "تعداد در مجموعه"])

        self.layout = QtWidgets.QVBoxLayout(Form)
        self.layoutTop = QtWidgets.QHBoxLayout()
        self.layoutDown = QtWidgets.QHBoxLayout()
        self.layoutTop.setContentsMargins(600, 0, 0, 30)
        self.layout.setContentsMargins(50, 10, 50, 10)
        self.layoutDown.setContentsMargins(0, 30, 0, 0)
        self.layoutDown.setSpacing(100)
        self.layout.addLayout(self.layoutTop)
        self.layout.addWidget(self.tableWidget1)
        self.layout.addLayout(self.layoutDown)

        self.layoutTop.addWidget(self.comboList)
        self.layoutDown.addWidget(self.cancelButton)
        self.layoutDown.addWidget(self.editButton)
        self.layoutDown.addWidget(self.newButton)

        self.refreshing_combolist_combination()
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect('equipment _data.db')
        cur = connection.cursor()
        cur1 = connection.cursor()
        while self.tableWidget1.rowCount() > 0:
            self.tableWidget1.removeRow(0)
        if len(self.combination_list) != 0:
            for item in self.combination_list:
                if self.comboList.currentText() == item:
                    index = self.combination_list.index(item)
                    self.id = self.combination_codelist[index]
            while self.tableWidget1.rowCount() > 0:
                self.tableWidget1.removeRow(0)
            for row in cur.execute(f'SELECT*FROM combination WHERE id ={self.id}'):
                for row1 in cur1.execute(f'SELECT *FROM equipment WHERE id ={row[4]}'):
                    rows = self.tableWidget1.rowCount()
                    self.tableWidget1.setRowCount(rows + 1)
                    self.tableWidget1.setItem(rows, 0, QTableWidgetItem(str(row1[0])))
                    self.tableWidget1.hideColumn(0)
                    self.tableWidget1.setItem(rows, 1, QTableWidgetItem(str(row1[1])))
                    self.tableWidget1.setItem(rows, 2, QTableWidgetItem(str(row1[2])))
                    self.tableWidget1.setItem(rows, 3, QTableWidgetItem(str(row1[3])))
                    self.tableWidget1.setItem(rows, 4, QTableWidgetItem(str(row[5])))
            self.tableWidget1.setWordWrap(True)
            self.tableWidget1.setColumnWidth(1, 350)


    def new_combination_box(self):
        window = new_combination()
        window.setupUi(window)
        window.exec_()
        self.refreshing_combolist_combination()
        self.load_data()

    def refreshing_combolist_combination(self):
        cur = self.connection.cursor()
        query = f"SELECT *FROM combination GROUP BY id"
        self.combination_list = []
        self.combination_codelist = []

        for row in cur.execute(query):
            name = str(row[1]) + " " + str(row[2]) + "  " + str(row[3])
            self.combination_list.append(name)
            self.combination_codelist.append(row[0])
        self.comboList.clear()
        self.comboList.addItems(self.combination_list)

    def edit_combination_box(self):
        window = editCombination()
        window.setupUi(window)
        window.exec_()
        self.refreshing_combolist_combination()
        self.load_data()

class editCombination(QtWidgets.QDialog):
    def setupUi(self, Form):
        font = QtGui.QFont("B Nazanin", 12)
        Form.setFont(font)

        self.connection = sqlite3.connect('equipment _data.db')

        Form.setObjectName("مدیریت مجموعه ها")
        Form.setWindowTitle("اصلاح مجموعه ها")
        Form.resize(700, 500)

        self.comboList = QtWidgets.QComboBox(Form)
        self.comboList.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.comboList.currentIndexChanged.connect(self.refreshing_table1)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("جستجو                                        ")
        self.lineEdit.textChanged.connect(self.searcher)

        self.tableWidget1 = QtWidgets.QTableWidget(Form)
        self.tableWidget1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget1.setObjectName("tableWidget")
        self.tableWidget1.setColumnCount(5)
        self.tableWidget1.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری", "تعداد در مجموعه"])

        # Set up the view table 2 and load the data
        self.tableWidget2 = QtWidgets.QTableWidget(Form)
        self.tableWidget2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget2.setObjectName("tableWidget")
        self.tableWidget2.setColumnCount(4)
        self.tableWidget2.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری"])

        self.cancelButton = QtWidgets.QPushButton(Form)
        self.cancelButton.setText("خروج")
        self.cancelButton.clicked.connect(lambda: self.close())

        self.newButton = QtWidgets.QPushButton(Form)
        self.newButton.setText("اصلاح مجموعه")
        self.newButton.clicked.connect(self.edit)

        self.editButton = QtWidgets.QPushButton(Form)
        self.editButton.setText("حذف مجموعه")
        self.editButton.clicked.connect(self.delete)

        QtCore.QMetaObject.connectSlotsByName(Form)
        self.refreshing_combolist_combination()
        self.load_data()
        self.tableWidget2.doubleClicked.connect(lambda: self.adding_to_table())

        # page layout
        self.layout = QtWidgets.QVBoxLayout(Form)
        self.layoutTop = QtWidgets.QVBoxLayout()
        self.layoutDown = QtWidgets.QHBoxLayout()
        self.layoutTop.setContentsMargins(500, 10, 0, 0)
        self.layoutTop.setSpacing(20)
        self.layout.setContentsMargins(50, 0, 50, 50)
        self.layoutDown.setSpacing(100)
        self.layout.addLayout(self.layoutTop)

        self.layout.addWidget(self.tableWidget2)
        self.layout.addWidget(self.tableWidget1)

        self.layout.addLayout(self.layoutDown)

        self.layoutTop.addWidget(self.comboList)
        self.layoutTop.addWidget(self.lineEdit)
        self.layoutDown.addWidget(self.cancelButton)
        self.layoutDown.addWidget(self.editButton)
        self.layoutDown.addWidget(self.newButton)

    def searcher(self):
        connection = sqlite3.connect('equipment _data.db')
        search = '%' + self.lineEdit.text() + '%'
        cur = connection.cursor()
        while self.tableWidget2.rowCount() > 0:
            self.tableWidget2.removeRow(0)
        for row in cur.execute(f"SELECT *FROM equipment WHERE item  LIKE '{search}'"):
            rows = self.tableWidget2.rowCount()
            self.tableWidget2.setRowCount(rows + 1)
            self.tableWidget2.setItem(rows, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget2.hideColumn(0)
            self.tableWidget2.setItem(rows, 1, QTableWidgetItem(str(row[1])))
            self.tableWidget2.setItem(rows, 2, QTableWidgetItem(str(row[2])))
            self.tableWidget2.setItem(rows, 3, QTableWidgetItem(str(row[3])))
        self.tableWidget2.resizeColumnsToContents()

    def load_data(self):
        cur = self.connection.cursor()
        while self.tableWidget2.rowCount() > 0:
            self.tableWidget2.removeRow(0)
        for row in cur.execute('SELECT*FROM equipment'):
            rows = self.tableWidget2.rowCount()
            self.tableWidget2.setRowCount(rows + 1)
            self.tableWidget2.setItem(rows, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget2.hideColumn(0)
            self.tableWidget2.setItem(rows, 1, QTableWidgetItem(str(row[1])))
            self.tableWidget2.setItem(rows, 2, QTableWidgetItem(str(row[2])))
            self.tableWidget2.setItem(rows, 3, QTableWidgetItem(str(row[3])))
        self.tableWidget2.resizeColumnsToContents()
        self.tableWidget2.setColumnWidth(1, 350)
        self.refreshing_table1()

    def refreshing_table1(self):
        cur = self.connection.cursor()
        cur1 = self.connection.cursor()
        while self.tableWidget1.rowCount() > 0:
            self.tableWidget1.removeRow(0)
        if len(self.combination_list) != 0:
            for item in self.combination_list:
                if self.comboList.currentText() == item:
                    index = self.combination_list.index(item)
                    self.id = self.combination_codelist[index]
            for row in cur.execute(f'SELECT*FROM combination WHERE id ={self.id}'):
                for row1 in cur1.execute(f'SELECT *FROM equipment WHERE id ={row[4]}'):
                    rows = self.tableWidget1.rowCount()
                    self.tableWidget1.setRowCount(rows + 1)
                    self.tableWidget1.setItem(rows, 0, QTableWidgetItem(str(row1[0])))
                    self.tableWidget1.hideColumn(0)
                    self.tableWidget1.setItem(rows, 1, QTableWidgetItem(str(row1[1])))
                    self.tableWidget1.setItem(rows, 2, QTableWidgetItem(str(row1[2])))
                    self.tableWidget1.setItem(rows, 3, QTableWidgetItem(str(row1[3])))
                    self.tableWidget1.setItem(rows, 4, QTableWidgetItem(str(row[5])))
        self.tableWidget1.resizeColumnsToContents()
        self.tableWidget1.setColumnWidth(1, 350)

    def adding_to_table(self):
        row = self.tableWidget2.currentRow()
        item = self.tableWidget2.item(row, 0)
        cur = self.connection.cursor()
        check = False
        row = 0
        while self.tableWidget1.item(row, 0) is not None:
            print(self.tableWidget1.item(row, 0).text(), item.text())
            if self.tableWidget1.item(row, 0).text() == item.text():
                check = True
                break
            row += 1
        if not check:
            query = f"SELECT *FROM equipment WHERE id = {item.text()}"
            for row in cur.execute(query):
                rows = self.tableWidget1.rowCount()
                self.tableWidget1.setRowCount(rows + 1)
                self.tableWidget1.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                self.tableWidget1.hideColumn(0)
                self.tableWidget1.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                self.tableWidget1.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                self.tableWidget1.setItem(rows, 3, QTableWidgetItem(str(row[3])))

    def refreshing_combolist_combination(self):
        cur = self.connection.cursor()
        query = f"SELECT *FROM combination GROUP BY id"
        self.combination_list = []
        self.combination_codelist = []

        for row in cur.execute(query):
            name = str(row[1]) + " " + str(row[2]) + "  " + str(row[3])
            self.combination_list.append(name)
            self.combination_codelist.append(row[0])

        self.comboList.clear()
        self.comboList.addItems(self.combination_list)

    # def deleting_item_data(self):
    #     row = self.tableWidget1.currentRow()
    #     item = self.tableWidget1.item(row, 0)
    #     connection = sqlite3.connect('equipment _data.db')
    #     cur = connection.cursor()
    #     cur.execute(f"DELETE FROM combination WHERE item=(?)", (item.text(),))
    #     connection.commit()
    #     self.tableWidget1.removeRow(int(row))

    def edit(self, item):
        check = True
        cur = self.connection.cursor()
        for item in self.combination_list:
            if self.comboList.currentText() == item:
                index = self.combination_list.index(item)
                self.id = self.combination_codelist[index]

        query = f'SELECT *FROM combination WHERE id ={self.id}'
        for row in (cur.execute(query)):
            self.name = row[1]
            self.size = row[2]
            self.pn = row[3]

        row = 0
        while self.tableWidget1.item(row, 0) is not None:
            try:
                pcs = self.tableWidget1.item(row, 4).text()
                pcs = int(pcs)
                row += 1
            except:
                self.tableWidget1.selectRow(row)
                QMessageBox.critical(None, "خطا", 'تعداد غیر مجاز وارد شده است.')
                check = False
                break
        if check:
            cur.execute(f"DELETE FROM combination WHERE id ={self.id}")
            self.connection.commit()
            row = 0
            while self.tableWidget1.item(row, 0) is not None:
                item = self.tableWidget1.item(row, 0).text()
                pcs = self.tableWidget1.item(row, 4).text()
                if pcs != "0":
                    cur.execute(f"INSERT INTO combination (id,name,size,pn,item,PcsPerCom) VALUES (?,?,?,?,?,?)",
                                (self.id, self.name, self.size, self.pn, item, pcs))
                    row += 1
                if pcs == "0": row+=1
            self.connection.commit()
            self.refreshing_table1()

    def delete(self, item):
        connection = sqlite3.connect('equipment _data.db')
        cur = connection.cursor()
        for row in cur.execute('SELECT * FROM ProjectName'):
            table_name = row[0].replace(" ", "_")
            table2 = "_" + table_name + "_2"
            cur.execute(f'DELETE FROM {table2} where id = {self.id}')
        cur = connection.cursor()
        for item in self.combination_list:
            if self.comboList.currentText() == item:
                index = self.combination_list.index(item)
                self.id = self.combination_codelist[index]
        cur.execute(f"DELETE FROM combination WHERE id ={self.id}")
        connection.commit()
        self.refreshing_combolist_combination()
        self.refreshing_table1()

class new_combination(QtWidgets.QDialog):
    def setupUi(self, Form):
        font = QtGui.QFont("B Nazanin", 12)
        Form.setFont(font)

        self.connection = sqlite3.connect('equipment _data.db')
        Form.setObjectName("Form")
        Form.setWindowTitle("مجموعه جدید")
        Form.resize(700, 500)
        Form.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.lineEdit0 = QtWidgets.QLineEdit(Form)
        self.lineEdit0.setObjectName("lineEdit")
        self.lineEdit0.setPlaceholderText("جستجو                                        ")
        self.lineEdit0.setAlignment(QtCore.Qt.AlignRight)



        self.lineEdit0.textChanged.connect(self.searcher)

        self.tableWidget1 = QtWidgets.QTableWidget(Form)
        self.tableWidget1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget1.setObjectName("tableWidget")
        self.tableWidget1.setColumnCount(5)
        self.tableWidget1.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری", "تعداد در مجموعه"])

        # Set up the view table 2 and load the data

        self.tableWidget2 = QtWidgets.QTableWidget(Form)
        self.tableWidget2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget2.setObjectName("tableWidget")
        self.tableWidget2.setColumnCount(4)
        self.tableWidget2.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری"])

        self.produceButton = QtWidgets.QPushButton(Form)

        self.pushButton3 = QtWidgets.QPushButton(Form)
        self.pushButton3.clicked.connect(lambda: self.close())

        font = QtGui.QFont()
        font.setPointSize(10)
        self.produceButton.setFont(font)
        self.produceButton.setObjectName("pushButton")
        self.produceButton.clicked.connect(self.produce)

        self.label = QtWidgets.QLabel(Form)
        self.label.setText("نام مجموعه:")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight)
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit.returnPressed.connect(lambda: self.lineEdit.text())

        self.labelsize = QtWidgets.QLabel(Form)
        self.labelsize.setText("سایز:")
        self.linesize = QtWidgets.QLineEdit(Form)
        self.linesize.setAlignment(QtCore.Qt.AlignRight)
        self.linesize.setObjectName("lineEdit")

        self.labelpn = QtWidgets.QLabel(Form)
        self.labelpn.setText("فشار:")

        self.linepn = QtWidgets.QLineEdit(Form)
        self.linepn.setAlignment(QtCore.Qt.AlignRight)
        self.linepn.setObjectName("lineEdit")

        self.layout = QtWidgets.QVBoxLayout(Form)
        self.layoutTop = QtWidgets.QHBoxLayout()
        self.layoutMiddel =QtWidgets.QVBoxLayout()
        self.layoutDown = QtWidgets.QHBoxLayout()
        self.layoutTop.setContentsMargins(500, 50, 50, 50)
        self.layoutTop.setContentsMargins(50, 50, 50, 50)
        self.layoutDown.setContentsMargins(200, 10, 200, 10)
        self.layoutMiddel.setContentsMargins(500, 10, 0, 10)
        self.layoutDown.setSpacing(100)

        self.layout.addLayout(self.layoutTop)

        self.layout.addLayout((self.layoutMiddel))
        self.layout.addWidget(self.tableWidget2)
        self.layout.addWidget(self.tableWidget1)

        self.layout.addLayout(self.layoutDown)

        self.layoutTop.addWidget(self.label)
        self.layoutTop.addWidget(self.lineEdit)
        self.layoutTop.addWidget(self.labelsize)
        self.layoutTop.addWidget(self.linesize)
        self.layoutTop.addWidget(self.labelpn)
        self.layoutTop.addWidget(self.linepn)
        self.layoutMiddel.addWidget(self.lineEdit0)
        self.layoutDown.addWidget(self.produceButton)
        self.layoutDown.addWidget(self.pushButton3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.load_data()
        self.tableWidget2.doubleClicked.connect(lambda: self.adding_to_table())

    def searcher(self):
        connection = sqlite3.connect('equipment _data.db')
        search = '%' + self.lineEdit0.text() + '%'
        cur = connection.cursor()
        while self.tableWidget2.rowCount() > 0:
            self.tableWidget2.removeRow(0)
        for row in cur.execute(f"SELECT *FROM equipment WHERE item  LIKE '{search}'"):
            rows = self.tableWidget2.rowCount()
            self.tableWidget2.setRowCount(rows + 1)
            self.tableWidget2.setItem(rows, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget2.hideColumn(0)
            self.tableWidget2.setItem(rows, 1, QTableWidgetItem(str(row[1])))
            self.tableWidget2.setItem(rows, 2, QTableWidgetItem(str(row[2])))
            self.tableWidget2.setItem(rows, 3, QTableWidgetItem(str(row[3])))
        self.tableWidget2.resizeColumnsToContents()

    def load_data(self):
        cur = self.connection.cursor()
        while self.tableWidget1.rowCount() > 0:
            self.tableWidget1.removeRow(0)
        n = 0

        for row in cur.execute('SELECT*FROM equipment'):
            rows = self.tableWidget2.rowCount()
            self.tableWidget2.setRowCount(rows + 1)
            self.tableWidget2.setItem(rows, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget2.hideColumn(0)
            self.tableWidget2.setItem(rows, 1, QTableWidgetItem(str(row[1])))
            self.tableWidget2.setItem(rows, 2, QTableWidgetItem(str(row[2])))
            self.tableWidget2.setItem(rows, 3, QTableWidgetItem(str(row[3])))
        self.tableWidget2.resizeColumnsToContents()
        self.tableWidget2.setColumnWidth(1, 450)


    def adding_to_table(self):
        row = self.tableWidget2.currentRow()
        item = self.tableWidget2.item(row, 0)
        connection = sqlite3.connect('equipment _data.db')
        cur = connection.cursor()
        check = False
        row = 0
        while self.tableWidget1.item(row, 0) is not None:
            if self.tableWidget1.item(row, 0).text() == item.text():
                check = True
                break
            row += 1

        if not check:
            query = f"SELECT *FROM equipment WHERE id = {item.text()}"
            for row in cur.execute(query):
                rows = self.tableWidget1.rowCount()
                self.tableWidget1.setRowCount(rows + 1)
                self.tableWidget1.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                self.tableWidget1.hideColumn(0)
                self.tableWidget1.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                self.tableWidget1.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                self.tableWidget1.setItem(rows, 3, QTableWidgetItem(str(row[3])))

    def produce(self, item):
        check = True
        cur = self.connection.cursor()
        query = 'SELECT MAX(id) AS next FROM combination'
        for row in (cur.execute(query)):
            if row[0] == None:
                self.id = 1
            else:
                self.id = int(row[0]) + 1
        if self.lineEdit.text() == "":
            self.lineEdit.setFocus()
            QMessageBox.critical(None, "خطا", 'نام پروژه را وارد نمایید.')
            check = False
        row = 0
        while self.tableWidget1.item(row, 0) is not None:
            try:
                pcs = self.tableWidget1.item(row, 4).text()
                pcs = int(pcs)
                row += 1
            except:
                self.tableWidget1.selectRow(row)
                QMessageBox.critical(None, "خطا", 'تعداد غیر مجاز وارد شده است.')
                check = False
                break

        if check:
            cur.execute(f"DELETE FROM combination WHERE id ={self.id}")
            self.connection.commit()
            row = 0
            while self.tableWidget1.item(row, 0) is not None:
                item = self.tableWidget1.item(row, 0).text()
                pcs = self.tableWidget1.item(row, 4).text()
                if pcs != "0":
                    cur.execute(f"INSERT INTO combination (id,name,size,pn,item,PcsPerCom) VALUES (?,?,?,?,?,?)",
                                (self.id, self.lineEdit.text(), self.linesize.text(), self.linepn.text(), item, pcs))
                    row += 1
            self.lineEdit.clear()
            self.linesize.clear()
            self.linepn.clear()
            self.connection.commit()
            while self.tableWidget1.rowCount() > 0:
                self.tableWidget1.removeRow(0)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "مجموعه جدید"))
        self.produceButton.setText(_translate("Form", "تولید"))
        self.label.setText(_translate("Form", "نام مجموعه:"))
        self.pushButton3.setText(_translate("Form", "خروج"))


