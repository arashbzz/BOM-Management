import sqlite3
import sys
import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PyQt5.Qt import QSize

class combination_managment(QtWidgets.QDialog):
    def setupUi(self, Form):
        font = QtGui.QFont("B Nazanin", 12)
        Form.setFont(font)
        self.connection = sqlite3.connect('equipment _data.db')

        Form.setObjectName("مدیریت آیتم ها")
        Form.setWindowTitle("مدیریت آیتم ها")

        self.cancelButton = QtWidgets.QPushButton(Form)
        self.cancelButton.setText("خروج")
        self.cancelButton.clicked.connect(lambda: self.close())

        self.saveButton = QtWidgets.QPushButton(Form)
        self.saveButton.setText("ذخیره")
        self.saveButton.clicked.connect(self.save)

        circle_style = "QPushButton {" \
                       "border-radius : 10;" \
                       "border : 1px solid grey}" \
                       "QPushButton:pressed {" \
                       "border-color : black;}"
        self.button_add = QtWidgets.QPushButton()
        self.button_del = QtWidgets.QPushButton()
        self.button_add.setIcon(QIcon('icons/plus.png'))
        self.button_del.setIcon(QIcon('icons/minus.png'))
        self.button_add.resize(20,20)
        self.button_del.resize(20,20)
        self.button_add.setIconSize(QSize(20,20))
        self.button_del.setIconSize(QSize(20,20))
        self.button_add.setStyleSheet(circle_style)
        self.button_del.setStyleSheet(circle_style)
        self.button_add.clicked.connect(self.select_add)
        self.button_del.clicked.connect(self.select_del)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("جستجو                                                             ")
        self.lineEdit.textChanged.connect(self.searcher)

        self.tableWidget1 = QtWidgets.QTableWidget(Form)
        self.tableWidget1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget1.setObjectName("tableWidget")
        self.tableWidget1.setColumnCount(6)
        self.tableWidget1.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری", "واحد", "قیمت"])
        # self.tableWidget1.contextMenuPolicy()

        self.layout = QtWidgets.QVBoxLayout(Form)
        self.layoutTop = QtWidgets.QHBoxLayout()
        self.layoutmiddel= QtWidgets.QHBoxLayout()
        self.layoutDown = QtWidgets.QHBoxLayout()
        self.layoutTop.setContentsMargins(10, 0, 0, 10)
        self.layoutmiddel.setContentsMargins(10, 10, 600, 0)
        self.layout.setContentsMargins(50, 10, 50, 10)
        self.layoutDown.setContentsMargins(0, 30, 0, 0)
        self.layoutDown.setSpacing(500)
        self.layoutTop.setSpacing(500)
        self.layout.addLayout(self.layoutTop)
        self.layout.addLayout(self.layoutmiddel)
        self.layout.addWidget(self.tableWidget1)
        self.layout.addLayout(self.layoutDown)

        self.layoutmiddel.addWidget(self.button_add)
        self.layoutmiddel.addWidget(self.button_del)
        self.layoutTop.addWidget(self.lineEdit)

        self.layoutDown.addWidget(self.cancelButton)
        # self.layoutDown.addWidget(self.editButton)
        self.layoutDown.addWidget(self.saveButton)

        self.last_id()
        self.load_data()

    def contextMenuEvent(self, event):
        selected_rows = self.tableWidget1.selectedItems()
        self.menu = QtWidgets.QMenu(self)
        addAction = QtWidgets.QAction('add', self)
        deleteAction = QtWidgets.QAction('delete', self)
        addAction.triggered.connect(lambda: self.addSlot(selected_rows))
        deleteAction.triggered.connect(lambda: self.deleteSlot(selected_rows))

        self.menu.addAction(addAction)
        self.menu.addAction(deleteAction)
        self.menu.popup(QtGui.QCursor.pos())
    def select_add(self):
        selected_rows = self.tableWidget1.selectedItems()
        self.addSlot(selected_rows)

    def select_del(self):
        selected_rows = self.tableWidget1.selectedItems()
        self.deleteSlot(selected_rows)

    def addSlot(self, selected_rows):
        n = 0
        b = []
        for i in selected_rows:
            n += 1
            b.append(i.row())

        for i in range(0, n):
            self.tableWidget1.insertRow(b[0])
            i += 1
            self.tableWidget1.setItem(b[0], 1, QTableWidgetItem(""))
            self.tableWidget1.setItem(b[0], 2, QTableWidgetItem(""))
            self.tableWidget1.setItem(b[0], 3, QTableWidgetItem(""))
            self.tableWidget1.setItem(b[0], 4, QTableWidgetItem(""))
            self.tableWidget1.setItem(b[0], 5, QTableWidgetItem(""))

    def deleteSlot(self, selected_rows):
        for i in selected_rows:
            self.tableWidget1.removeRow(i.row())

    def load_data(self):
        connection = sqlite3.connect('equipment _data.db')
        cur = connection.cursor()
        while self.tableWidget1.rowCount() > 0:
            self.tableWidget1.removeRow(0)
        for row in cur.execute(f'SELECT*FROM equipment'):
            rows = self.tableWidget1.rowCount()
            self.tableWidget1.setRowCount(rows + 1)
            self.tableWidget1.setItem(rows, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget1.hideColumn(0)
            self.tableWidget1.setItem(rows, 1, QTableWidgetItem(str(row[1])))
            self.tableWidget1.setItem(rows, 2, QTableWidgetItem(str(row[2])))
            self.tableWidget1.setItem(rows, 3, QTableWidgetItem(str(row[3])))
            self.tableWidget1.setItem(rows, 4, QTableWidgetItem(str(row[4])))
            self.tableWidget1.setItem(rows, 5, QTableWidgetItem(str(row[5])))
        self.tableWidget1.setWordWrap(True)
        self.tableWidget1.setColumnWidth(1, 300)

    def searcher(self):
        connection = sqlite3.connect('equipment _data.db')
        search = '%' + self.lineEdit.text() + '%'
        cur = connection.cursor()
        while self.tableWidget1.rowCount() > 0:
            self.tableWidget1.removeRow(0)
        for row in cur.execute(f"SELECT *FROM equipment WHERE item  LIKE '{search}'"):
            rows = self.tableWidget1.rowCount()
            self.tableWidget1.setRowCount(rows + 1)
            self.tableWidget1.setItem(rows, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget1.hideColumn(0)
            self.tableWidget1.setItem(rows, 1, QTableWidgetItem(str(row[1])))
            self.tableWidget1.setItem(rows, 2, QTableWidgetItem(str(row[2])))
            self.tableWidget1.setItem(rows, 3, QTableWidgetItem(str(row[3])))
            self.tableWidget1.setItem(rows, 4, QTableWidgetItem(str(row[4])))
            self.tableWidget1.setItem(rows, 5, QTableWidgetItem(str(row[5])))
        self.tableWidget1.resizeColumnsToContents()

    def last_id(self):
        cur = self.connection.cursor()
        id_list = []
        query = 'SELECT * FROM equipment'
        for row in cur.execute(query):
            id_list.append(row[0])
            self.max_id = id_list[len(id_list) - 1]

    def save(self, item):
        cur = self.connection.cursor()
        id_list = []
        remove_id = []

        query = 'SELECT * FROM equipment'
        for row in cur.execute(query):
            id_list.append(row[0])
        id_list.sort()
        for i in range(len(id_list) - 1):
            if id_list[i + 1] - id_list[i] != 1:
                remove_id.append(id_list[i])

        for row in cur.execute('SELECT * FROM ProjectName'):
            table_name = row[0].replace(" ", "_")
            table1 = "_" + table_name + "_1"
            for i in remove_id:
                cur.execute(f'DELETE FROM {table1} where id = {i}')
                cur.execute(f'DELETE FROM combination where item = {i}')

        cur.execute(f"DELETE FROM equipment ")
        self.connection.commit()

        row = 0
        while self.tableWidget1.rowCount() > 0:

            if self.tableWidget1.item(0, 0) is None:
                id = self.max_id + 1
                self.max_id += 1

            else:
                id = self.tableWidget1.item(0, 0).text()
            item = self.tableWidget1.item(0, 1).text()
            size = self.tableWidget1.item(0, 2).text()
            pn = self.tableWidget1.item(0, 3).text()
            unit = self.tableWidget1.item(0, 4).text()
            price = self.tableWidget1.item(0, 5).text()
            self.tableWidget1.removeRow(0)
            cur.execute(f"INSERT INTO equipment (id,item,size,pn,unit,price) VALUES (?,?,?,?,?,?)",
                        (id, item, size, pn, unit,price))
            row += 1
        self.connection.commit()
        self.load_data()
