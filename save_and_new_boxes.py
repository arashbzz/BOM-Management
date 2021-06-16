import xlwt
import sqlite3
import sys
import os
from PyQt5 import QtCore, QtWidgets, QtGui

class LoadBox(QtWidgets.QDialog):
    def setupUi(self, Form):
        font = QtGui.QFont("B Nazanin", 12)
        Form.setFont(font)
        connection = sqlite3.connect('equipment _data.db')
        cur = connection.cursor()
        query = 'SELECT * FROM ProjectName'
        cur.execute(query)
        self.project_list = []
        for row in cur.execute(query):
            self.project_list.append(row[0])
        Form.setObjectName("Form")

        Form.resize(300, 200)
        Form.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.addItems(self.project_list)
        self.listWidget.clicked.connect(self.list_clicked)

        self.pushButton = QtWidgets.QPushButton(Form)

        self.pushButton3 = QtWidgets.QPushButton(Form)
        self.pushButton3.clicked.connect(lambda: self.close())

        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.project_deleting)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.pushButton.clicked.connect(self.ok_push)

        self.layout = QtWidgets.QVBoxLayout(Form)
        self.layoutDown = QtWidgets.QHBoxLayout()

        self.layout.setContentsMargins(30, 10, 30, 10)
        self.layoutDown.setContentsMargins(0, 30, 0, 0)
        self.layoutDown.setSpacing(50)
        self.layout.addWidget((self.label))
        self.layout.addWidget((self.lineEdit))
        self.layout.addWidget(self.listWidget)
        self.layout.addLayout(self.layoutDown)

        self.layoutDown.addWidget(self.pushButton)
        self.layoutDown.addWidget(self.pushButton_2)
        self.layoutDown.addWidget(self.pushButton3)


    def project_deleting(self):

        connection = sqlite3.connect('equipment _data.db')
        cur = connection.cursor()
        if self.listWidget.currentItem() != None:
            cur.execute(f"DELETE FROM ProjectName WHERE name = '{self.listWidget.currentItem().text()}'")

            self.project_name = self.listWidget.currentItem().text()
            table_name =self.project_name.replace(" ", "_")
            self.table1 = "_"+ table_name + "_1"
            self.table2 = "_"+ table_name + "_2"
            self.table3 = "_"+ table_name + "_3"
            cur.execute(f"DROP TABLE {self.table1}")
            cur.execute(f"DROP TABLE {self.table2}")
            cur.execute(f"DROP TABLE {self.table3}")

            for item in self.project_list:
                if item == self.listWidget.currentItem().text():
                    self.project_list.remove(item)
                    self.listWidget.takeItem(self.listWidget.currentRow())
            connection.commit()

    def list_clicked(self):
        self.selected = self.project_list[self.listWidget.currentRow()]
        self.lineEdit.setText(self.selected)

    def ok_push(self):
        if self.lineEdit.text() != "":
            self.close()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "بارگزاری"))
        self.pushButton.setText(_translate("Form", "اجرا"))
        self.label.setText(_translate("Form", "نام پروژه:"))
        self.pushButton_2.setText(_translate("Form", "حذف"))
        self.pushButton3.setText(_translate("Form", "خروج"))

class SaveBox(QtWidgets.QDialog):
    def setupUi(self, Form):
        font = QtGui.QFont("B Nazanin", 12)
        Form.setFont(font)
        Form.setObjectName("Form")
        Form.resize(300, 200)
        Form.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.close())
        self.pushButton = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.pushButton.clicked.connect(self.ok_push)

        self.layout = QtWidgets.QVBoxLayout(Form)
        self.layoutUp = QtWidgets.QHBoxLayout()
        self.layoutMiddel = QtWidgets.QHBoxLayout()
        self.layoutDown = QtWidgets.QHBoxLayout()

        self.layout.setContentsMargins(30, 10, 30, 10)
        self.layoutDown.setContentsMargins(0, 10, 0, 0)
        self.layoutDown.setSpacing(50)
        self.layout.addLayout(self.layoutUp)
        self.layout.addLayout(self.layoutMiddel)
        self.layout.addLayout(self.layoutDown)

        self.layoutUp.addWidget(self.label)
        self.layoutUp.addWidget(self.lineEdit)
        self.layoutMiddel.addWidget(self.label_2)
        self.layoutMiddel.addWidget(self.lineEdit_2)
        self.layoutDown.addWidget(self.pushButton)
        self.layoutDown.addWidget(self.pushButton_2)


    def ok_push(self):
        if self.lineEdit.text() != "":
            self.close()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "پروژه جدید"))
        self.pushButton.setText(_translate("Form", "ذخیره"))
        self.label.setText(_translate("Form", "نام پروژه:"))
        self.label_2.setText(_translate("Form", "نام کارفرما:"))
        self.pushButton_2.setText(_translate("Form", "خروج"))