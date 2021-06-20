import sqlite3
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QMessageBox,
    QTableWidgetItem,
    QLabel
)
from PyQt5.Qt import QSize
import new_combination
import new_item
import save_and_new_boxes
import print_box
import excel_box


# class Login(QtWidgets.QDialog):
#     def __init__(self, parent=None):
#         super(Login, self).__init__(parent)
#         self.textName = QtWidgets.QLineEdit(self)
#         self.textPass = QtWidgets.QLineEdit(self)
#         self.buttonLogin = QtWidgets.QPushButton('Login', self)
#         self.buttonLogin.clicked.connect(self.handleLogin)
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.addWidget(self.textName)
#         layout.addWidget(self.textPass)
#         layout.addWidget(self.buttonLogin)
#
#     def handleLogin(self):
#         if (self.textName.text() == '' and
#                 self.textPass.text() == ''):
#             self.accept()
#         else:
#             QtWidgets.QMessageBox.warning(
#                 self, 'Error', 'Bad user or password')
class InitialDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, decimals, parent=None):
        super().__init__(parent)
        self.nDecimals = decimals

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter
        try:
            text = index.model().data(index, QtCore.Qt.DisplayRole)
            number = float(text)
            option.text = "{:,.{}f}".format(number, self.nDecimals)
        except:
            pass


def about_win():
    about_form = QtWidgets.QDialog()
    about_form.setStyleSheet("background-color: rgb(255, 255, 255);")
    about_form.setWindowTitle("درباره برنامه")
    font = QtGui.QFont("B Nazanin", 12)
    label = QLabel(about_form)
    pixmap = QPixmap('icons/zistab_logo.jpg')
    pixmap = pixmap.scaledToWidth(100)
    label.setPixmap(pixmap)
    label.resize(pixmap.width(), pixmap.height())
    label.setStyleSheet("background-image: white;")

    label_1 = QLabel(about_form)
    logo = QPixmap('icons/logo.jpg')
    logo = logo.scaledToWidth(100)
    label_1.setPixmap(logo)
    label_1.resize(logo.width(), logo.height())

    label_2 = QLabel(about_form)
    label_2.setFont(font)
    label_2.setText(
        " برنامه مدیریت لیست لوازم \n\n این برنامه برای تهیه و مدیریت لیست لوازم پروژه های آبی می باشد.\n "
        "این نرم افزار مشمول قوانین کپی برداری بوده و کلیه حقوق مادی و معنوی آن متعلق به شرکت مهندسین "
        "مشاور زیستاب می باشد. هرگونه استفاده غیر مجاز از این نرم افزار پیگرد قانونی دارد.\n \n ویرایش:  1.0 \n   \n "
        "http:/www.zistab.com")

    layout = QtWidgets.QHBoxLayout(about_form)
    righlayout = QtWidgets.QHBoxLayout()
    middlelayout = QtWidgets.QHBoxLayout()
    leftlayout = QtWidgets.QHBoxLayout()

    righlayout.setContentsMargins(0,0,0,100)
    middlelayout.setContentsMargins(0, 0, 0, 0)
    leftlayout.setContentsMargins(0, 100, 0, 0)

    layout.addLayout(leftlayout)
    layout.addLayout((middlelayout))
    layout.addLayout(righlayout)
    leftlayout.addWidget(label)
    righlayout.addWidget(label_1)
    middlelayout.addWidget(label_2)

    label_2.setWordWrap(True)
    about_form.exec_()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        font = QtGui.QFont("B Nazanin", 12)
        MainWindow.setFont(font)
        self.connection = sqlite3.connect('equipment _data.db')
        self.project_name = None
        MainWindow.setObjectName("MainWindow")

        self.x = 1200
        self.y = 600
        MainWindow.resize(self.x, self.y)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)

        self.tabWidget.setEnabled(True)
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.label = QtWidgets.QLabel(self.tab_2)

        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")

        self.label0 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label0.setFont(font)
        self.label0.setTextFormat(QtCore.Qt.AutoText)
        self.label0.setObjectName("label")

        self.lineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight)
        self.lineEdit.setPlaceholderText(
            "جستجو                                                                           ")
        self.lineEdit.textChanged.connect(self.searcher)

        # Set up the view table 1 and load the data

        self.tableWidget1 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget1.setObjectName("tableWidget")
        self.tableWidget1.setColumnCount(4)
        self.tableWidget1.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری"])

        # Set up the view table 2 and load the data

        self.tableWidget2 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget2.setObjectName("tableWidget")
        self.tableWidget2.setColumnCount(4)
        self.tableWidget2.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری"])

        self.lineEdit1 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit1.setObjectName("lineEdit")
        self.lineEdit1.setAlignment(QtCore.Qt.AlignRight)
        self.lineEdit1.setPlaceholderText(
            "جستجو                                                                           ")
        self.lineEdit1.textChanged.connect(self.searcher_com)

        # Set up the view table 3

        self.tableWidget3 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget3.setObjectName("tableWidget")
        self.tableWidget3.setColumnCount(4)
        self.tableWidget3.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری"])

        # Set up the view table 4

        self.tableWidget4 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget4.setObjectName("tableWidget")
        self.tableWidget4.setColumnCount(4)
        self.tableWidget4.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری"])

        # Push buttons
        self.new_item = QtWidgets.QPushButton(self.tab_2)
        self.new_item.setObjectName("new_item")
        self.new_item.clicked.connect(self.new_item_box)
        self.new_component = QtWidgets.QPushButton(self.tab_2)
        self.new_component.setObjectName("new_component")
        self.new_component.clicked.connect(self.new_combination_box)

        ######  TAB_3  ######

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")

        # Set up the view table 5

        self.tableWidget5 = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget5.setObjectName("tableWidget")
        self.tableWidget5.setColumnCount(5)
        self.tableWidget5.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری", "تعداد"])

        # Set up the view table 6

        self.tableWidget6 = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget6.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget6.setObjectName("tableWidget")
        self.tableWidget6.setColumnCount(5)
        self.tableWidget6.setHorizontalHeaderLabels(["ID", "مجموعه", "سایز", "فشار کاری", "تعداد"])

        ######  TAB_5  ######

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.tableWidget7 = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget7.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget7.setObjectName("tableWidget")
        self.tableWidget7.setColumnCount(6)
        self.tableWidget7.setHorizontalHeaderLabels(["ID", "شرح", "سایز", "فشار کاری", "واحد", "تعداد"])
        self.result_button = QtWidgets.QPushButton(self.tab_5)
        self.result_button.setText("محاسبه")
        self.result_button.setObjectName("result")
        self.result_button.clicked.connect(self.inputting_item_pcs)

        ######  TAB_6  ######
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tabWidget.addTab(self.tab_6, "")

        self.tableWidget8 = QtWidgets.QTableWidget(self.tab_6)
        self.tableWidget8.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tableWidget8.setObjectName("tableWidget")
        self.tableWidget8.setColumnCount(8)
        self.tableWidget8.setHorizontalHeaderLabels(
            ["ID", "شرح", "سایز", "فشار کاری", "واحد", "تعداد", "قیمت", "قیمت کل"])
        self.result2_button = QtWidgets.QPushButton(self.tab_6)
        self.result2_button.setText("محاسبه")
        self.result2_button.setObjectName("result")
        self.result2_button.clicked.connect(self.total_price)

        ######  Menu Bar  ######
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.__file = QtWidgets.QMenu(self.menubar)
        self.__tools = QtWidgets.QMenu(self.menubar)
        self.__about = QtWidgets.QMenu(self.menubar)

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.acrion_1 = QtWidgets.QAction(MainWindow)
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_7 = QtWidgets.QAction(MainWindow)
        self.action_8 = QtWidgets.QAction(MainWindow)
        self.action_9 = QtWidgets.QAction(MainWindow)
        self.action_10 = QtWidgets.QAction(MainWindow)
        self.action_11 = QtWidgets.QAction(MainWindow)
        self.action_12 = QtWidgets.QAction(MainWindow)


        self.menubar.addAction(self.__file.menuAction())
        self.menubar.addAction(self.__tools.menuAction())
        self.menubar.addAction(self.__about.menuAction())


        self.__file.addAction(self.acrion_1)
        self.__file.addAction(self.action_2)
        self.__about.addAction(self.action_3)
        self.__file.addSeparator()
        self.__file.addAction(self.action_4)
        self.__about.addAction(self.action_5)
        self.__tools.addAction(self.action_7)
        self.__tools.addAction(self.action_9)
        self.__tools.addAction(self.action_10)
        self.__tools.addAction(self.action_12)

        self.acrion_1.triggered.connect(self.new_project_box)
        self.action_2.triggered.connect(self.load_project_box)
        self.action_4.triggered.connect(lambda: sys.exit(app.exec_()))
        self.action_5.triggered.connect(about_win)
        self.action_7.triggered.connect(self.to_excel)
        self.action_9.triggered.connect(self.new_combination_box)
        self.action_10.triggered.connect(self.new_item_box)
        self.action_12.triggered.connect(self.print)
        self.action_7.setEnabled(False)
        self.action_12.setEnabled(False)
        self.action_3.setEnabled(False)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        self.tableWidget1.doubleClicked.connect(
            lambda: self.adding_to_table(self.tableWidget1, self.tableWidget2, self.table1))
        self.tableWidget3.doubleClicked.connect(
            lambda: self.adding_to_table(self.tableWidget3, self.tableWidget4, self.table2))

        circle_style = "QPushButton {" \
                       "border-radius : 15;" \
                       "border : 1px solid grey}" \
                       "QPushButton:pressed {" \
                       "border-color : red;}"
        self.button_next_1 = QtWidgets.QPushButton(self.tab_2)
        self.button_next_2 = QtWidgets.QPushButton(self.tab_3)
        self.button_next_3 = QtWidgets.QPushButton(self.tab_5)
        self.button_next_1.setIcon(QIcon('icons/next_icon.png'))
        self.button_next_2.setIcon(QIcon('icons/next_icon.png'))
        self.button_next_3.setIcon(QIcon('icons/next_icon.png'))
        self.button_next_1.resize(30, 30)
        self.button_next_2.resize(30, 30)
        self.button_next_3.resize(30, 30)
        self.button_next_1.setIconSize(QSize(28,28))
        self.button_next_2.setIconSize(QSize(28, 28))
        self.button_next_3.setIconSize(QSize(28, 28))
        self.button_next_1.setStyleSheet(circle_style)
        self.button_next_2.setStyleSheet(circle_style)
        self.button_next_3.setStyleSheet(circle_style)

        self.button_next_1.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self.button_next_2.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.button_next_3.clicked.connect(lambda: self.tabWidget.setCurrentIndex(3))

        self.mainlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainlayout.addWidget(self.tabWidget)

        self.tabLayout = QtWidgets.QVBoxLayout(self.tab_2)
        self.tabLayout.setContentsMargins(40, 20, 40, 20)

        self.Layout1 = QtWidgets.QHBoxLayout(self.tab_2)
        self.Layout1.setContentsMargins(300, 20, 0, 0)
        self.Layout1.setSpacing(315)
        self.Layout2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.Layout2.setSpacing(20)
        self.Layout3 = QtWidgets.QHBoxLayout(self.tab_2)
        self.Layout3.setSpacing(20)
        self.Layout4 = QtWidgets.QHBoxLayout(self.tab_2)
        self.Layout4.setContentsMargins(0, 20, 450, 0)
        self.Layout4.setSpacing(454)

        self.Laynext_1 = QtWidgets.QVBoxLayout(self.tab_2)
        # self.tabLayout.addLayout(self.Laynext_1)
        self.Laynext_1.setContentsMargins(0, 0, 1100, 0)
        self.Laynext_1.addWidget(self.button_next_1)


        self.tabLayout.addWidget(self.label0)
        self.tabLayout.addWidget(self.label)
        self.tabLayout.addLayout(self.Layout1)
        self.tabLayout.addLayout(self.Layout2)
        self.tabLayout.addLayout(self.Layout3)
        self.tabLayout.addLayout(self.Layout4)

        self.Layout1.addWidget(self.lineEdit)
        self.Layout1.addWidget(self.lineEdit1)

        self.Layout2.addWidget(self.tableWidget1)
        self.Layout2.addWidget(self.tableWidget3)

        self.Layout3.addWidget(self.tableWidget2)
        self.Layout3.addWidget(self.tableWidget4)

        self.Layout4.addWidget(self.new_item)
        self.Layout4.addWidget(self.new_component)

        self.tab_2_Layout = QtWidgets.QGridLayout(self.tab_3)

        self.tab_2_Layout.setVerticalSpacing(15)
        self.tab_2_Layout.setHorizontalSpacing(50)

        self.tab_2_Layout.setContentsMargins(0, 50, 10, 10)
        self.tab_2_Layout.addWidget(self.tableWidget5, 2, 1)
        self.tab_2_Layout.addWidget(self.tableWidget6, 2, 2)

        self.tab_3_Layout = QtWidgets.QGridLayout(self.tab_5)

        self.tab_3_Layout.setVerticalSpacing(15)
        self.tab_3_Layout.setHorizontalSpacing(50)

        self.tab_3_Layout.setContentsMargins(300, 50, 10, 10)
        self.tab_3_Layout.addWidget(self.tableWidget7, 2, 1)
        self.tab_3_Layout.addWidget(self.result_button, 2, 3)

        self.tab_4_Layout = QtWidgets.QGridLayout(self.tab_6)

        self.tab_4_Layout.setVerticalSpacing(15)
        self.tab_4_Layout.setHorizontalSpacing(50)

        self.tab_4_Layout.setContentsMargins(200, 50, 10, 10)
        self.tab_4_Layout.addWidget(self.tableWidget8, 2, 1)
        self.tab_4_Layout.addWidget(self.result2_button, 2, 3)

        self.tableWidget2.doubleClicked.connect(self.deleting_item_data)
        self.tableWidget4.doubleClicked.connect(self.deleting_combination_data)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def searcher(self):
        if self.project_name != None:
            search = '%' + self.lineEdit.text() + '%'
            cur = self.connection.cursor()
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
            self.tableWidget1.resizeColumnsToContents()

    def searcher_com(self):
        if self.project_name != None:
            search = '%' + self.lineEdit1.text() + '%'
            cur = self.connection.cursor()
            while self.tableWidget3.rowCount() > 0:
                self.tableWidget3.removeRow(0)
            for row in cur.execute(f"SELECT *FROM combination WHERE name LIKE '{search}' GROUP BY id"):
                rows = self.tableWidget3.rowCount()
                self.tableWidget3.setRowCount(rows + 1)
                self.tableWidget3.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                self.tableWidget3.hideColumn(0)
                self.tableWidget3.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                self.tableWidget3.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                self.tableWidget3.setItem(rows, 3, QTableWidgetItem(str(row[3])))
            self.tableWidget3.resizeColumnsToContents()

    def inputting_item_pcs(self):
        row = 0
        check = True
        while self.tableWidget5.item(row, 0) is not None:
            try:
                item = self.tableWidget5.item(row, 0).text()
                changed_item = self.tableWidget5.item(row, 4).text()
                changed_item = int(changed_item)
                cur = self.connection.cursor()
                cur.execute(f"UPDATE '{self.table1}' SET pcs='{changed_item}' Where id = '{item}' ")
                row += 1
            except:
                self.tabWidget.setCurrentIndex(1)
                self.tableWidget5.selectRow(row)
                QMessageBox.critical(None, "خطا", 'تعداد غیر مجاز وارد شده است.')
                check = False
                break
        self.connection.commit()
        row = 0
        while self.tableWidget6.item(row, 0) is not None:
            item = self.tableWidget6.item(row, 0).text()
            changed_item = self.tableWidget6.item(row, 4).text()
            try:
                changed_item = int(changed_item)
                cur = self.connection.cursor()
                cur.execute(f"UPDATE '{self.table2}' SET pcs='{changed_item}' Where id = '{item}'")
                row += 1
            except:
                self.tabWidget.setCurrentIndex(1)
                self.tableWidget6.selectRow(row)
                QMessageBox.critical(None, "خطا", 'تعداد غیر مجاز وارد شده است.')
                check = False
                break
        self.connection.commit()
        if check:
            self.result()

    def adding_to_table(self, a, b, c):
        row = a.currentRow()
        item = a.item(row, 0)
        cur = self.connection.cursor()
        check = False
        for row in cur.execute(f"SELECT *FROM {c}"):

            if row[0] == item.text():
                check = True
                break
        if not check:
            if b == self.tableWidget2:
                cur.execute(f"INSERT INTO {c} (id) VALUES (?)", (item.text(),))
                query = f"SELECT *FROM equipment WHERE id = {item.text()}"
                self.connection.commit()
                for row in cur.execute(query):
                    rows = b.rowCount()
                    b.setRowCount(rows + 1)
                    b.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                    b.hideColumn(0)
                    b.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                    b.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                    b.setItem(rows, 3, QTableWidgetItem(str(row[3])))
                b.resizeColumnsToContents()
                self.refreshing_table5()

            elif b == self.tableWidget4:
                cur.execute(f"INSERT INTO {c} (id) VALUES (?)", (item.text(),))
                query = f"SELECT *FROM combination WHERE id = {item.text()} GROUP BY id"
                self.connection.commit()
                for row in cur.execute(query):
                    rows = b.rowCount()
                    b.setRowCount(rows + 1)
                    b.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                    b.hideColumn(0)
                    b.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                    b.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                    b.setItem(rows, 3, QTableWidgetItem(str(row[3])))
                b.resizeColumnsToContents()
                self.refreshing_table6()

    def load_data(self):
        try:
            cur = self.connection.cursor()

            while self.tableWidget1.rowCount() > 0:
                self.tableWidget1.removeRow(0)
            while self.tableWidget3.rowCount() > 0:
                self.tableWidget3.removeRow(0)

            for row in cur.execute('SELECT*FROM equipment'):
                rows = self.tableWidget1.rowCount()
                self.tableWidget1.setRowCount(rows + 1)
                self.tableWidget1.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                self.tableWidget1.hideColumn(0)
                self.tableWidget1.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                self.tableWidget1.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                self.tableWidget1.setItem(rows, 3, QTableWidgetItem(str(row[3])))
            self.tableWidget1.resizeColumnsToContents()

            for row in cur.execute('SELECT * FROM combination GROUP BY id'):
                rows = self.tableWidget3.rowCount()
                self.tableWidget3.setRowCount(rows + 1)
                self.tableWidget3.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                self.tableWidget3.hideColumn(0)
                self.tableWidget3.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                self.tableWidget3.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                self.tableWidget3.setItem(rows, 3, QTableWidgetItem(str(row[3])))
            self.tableWidget3.resizeColumnsToContents()

            self.refreshing_table2()  # loading table 2 from tab 1
            self.refreshing_table5()  # loading table 5 from tab 2
            self.refreshing_table4()  # loading table 4 from tab 1
            self.refreshing_table6()  # loading table 6 from tab 2

            self.label0.setText(f"نام طرج :  {self.project_name}")
        except: pass

    def deleting_item_data(self):
        row = self.tableWidget2.currentRow()
        item = self.tableWidget2.item(row, 0)
        cur = self.connection.cursor()
        cur.execute(f"DELETE FROM {self.table1} WHERE id=(?)", (item.text(),))
        self.connection.commit()
        self.tableWidget2.removeRow(int(row))
        self.refreshing_table5()

    def deleting_combination_data(self):
        row = self.tableWidget4.currentRow()
        item = self.tableWidget4.item(row, 0)
        cur = self.connection.cursor()
        cur.execute(f"DELETE FROM {self.table2} WHERE id=(?)", (item.text()))
        self.connection.commit()
        self.tableWidget4.removeRow(int(row))
        self.refreshing_table6()

    def refreshing_table5(self):
        cur = self.connection.cursor()
        cur1 = self.connection.cursor()
        while self.tableWidget5.rowCount() > 0:
            self.tableWidget5.removeRow(0)
        for ro in cur.execute(f"SELECT*FROM {self.table1}"):
            for row in cur1.execute(f"SELECT*FROM equipment WHERE id = {ro[0]}"):
                rows = self.tableWidget5.rowCount()
                self.tableWidget5.setRowCount(rows + 1)
                self.tableWidget5.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                self.tableWidget5.hideColumn(0)
                self.tableWidget5.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                self.tableWidget5.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                self.tableWidget5.setItem(rows, 3, QTableWidgetItem(str(row[3])))
                self.tableWidget5.setItem(rows, 4, QTableWidgetItem(str(ro[1])))
        self.tableWidget5.resizeColumnsToContents()

    def refreshing_table2(self):
        cur = self.connection.cursor()
        cur1 = self.connection.cursor()
        while self.tableWidget2.rowCount() > 0:
            self.tableWidget2.removeRow(0)
        for row1 in cur.execute(f"SELECT*FROM {self.table1}"):
            query = f"SELECT*FROM equipment WHERE id = {row1[0]}"
            for row in cur1.execute(query):
                rows = self.tableWidget2.rowCount()
                self.tableWidget2.setRowCount(rows + 1)
                self.tableWidget2.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                self.tableWidget2.hideColumn(0)
                self.tableWidget2.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                self.tableWidget2.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                self.tableWidget2.setItem(rows, 3, QTableWidgetItem(str(row[3])))
                self.tableWidget2.setItem(rows, 4, QTableWidgetItem(str(row1[1])))
        self.tableWidget2.resizeColumnsToContents()

    def refreshing_table4(self):
        cur = self.connection.cursor()
        cur1 = self.connection.cursor()
        while self.tableWidget4.rowCount() > 0:
            self.tableWidget4.removeRow(0)
        for row1 in cur.execute(f"SELECT*FROM {self.table2}"):
            query = f"SELECT*FROM combination WHERE id = {row1[0]} GROUP BY id"
            for row in cur1.execute(query):
                rows = self.tableWidget4.rowCount()
                self.tableWidget4.setRowCount(rows + 1)
                self.tableWidget4.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                self.tableWidget4.hideColumn(0)
                self.tableWidget4.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                self.tableWidget4.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                self.tableWidget4.setItem(rows, 3, QTableWidgetItem(str(row[3])))
        self.tableWidget4.resizeColumnsToContents()

    def refreshing_table6(self):
        cur = self.connection.cursor()
        cur1 = self.connection.cursor()
        while self.tableWidget6.rowCount() > 0:
            self.tableWidget6.removeRow(0)
        for row1 in cur.execute(f"SELECT*FROM {self.table2}"):
            query = f"SELECT*FROM combination WHERE id = {row1[0]} GROUP BY id"
            for row in cur1.execute(query):
                rows = self.tableWidget6.rowCount()
                self.tableWidget6.setRowCount(rows + 1)
                self.tableWidget6.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                self.tableWidget6.hideColumn(0)
                self.tableWidget6.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                self.tableWidget6.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                self.tableWidget6.setItem(rows, 3, QTableWidgetItem(str(row[3])))
                self.tableWidget6.setItem(rows, 4, QTableWidgetItem(str(row1[1])))
        self.tableWidget6.resizeColumnsToContents()

    def refreshing_table7(self):
        cur = self.connection.cursor()
        cur1 = self.connection.cursor()
        while self.tableWidget7.rowCount() > 0:
            self.tableWidget7.removeRow(0)
        for row2 in cur.execute(f"SELECT id, SUM(pcs) AS Total FROM {self.table3} GROUP BY id"):
            for row in cur1.execute(f"SELECT*FROM equipment WHERE id = {row2[0]} GROUP BY id"):
                rows = self.tableWidget7.rowCount()
                self.tableWidget7.setRowCount(rows + 1)
                self.tableWidget7.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                self.tableWidget7.hideColumn(0)
                self.tableWidget7.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                self.tableWidget7.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                self.tableWidget7.setItem(rows, 3, QTableWidgetItem(str(row[3])))
                self.tableWidget7.setItem(rows, 4, QTableWidgetItem(str(row[4])))
                self.tableWidget7.setItem(rows, 5, QTableWidgetItem(str(row2[1])))
        self.tableWidget7.resizeColumnsToContents()
        self.action_7.setEnabled(True)
        self.action_12.setEnabled(True)

    def refreshing_table8(self):
        cur = self.connection.cursor()
        cur1 = self.connection.cursor()
        while self.tableWidget8.rowCount() > 0:
            self.tableWidget8.removeRow(0)
        sum_sum = 0
        rows = 0
        break_sign = False
        for row2 in cur.execute(f"SELECT id, SUM(pcs), SUM(price_t) FROM {self.table3} GROUP BY id"):
            for row in cur1.execute(f"SELECT*FROM equipment WHERE id = {row2[0]} GROUP BY id"):
                rows = self.tableWidget8.rowCount()
                self.tableWidget8.setRowCount(rows + 1)
                self.tableWidget8.setItem(rows, 0, QTableWidgetItem(str(row[0])))
                self.tableWidget8.hideColumn(0)
                self.tableWidget8.setItem(rows, 1, QTableWidgetItem(str(row[1])))
                self.tableWidget8.setItem(rows, 2, QTableWidgetItem(str(row[2])))
                self.tableWidget8.setItem(rows, 3, QTableWidgetItem(str(row[3])))
                self.tableWidget8.setItem(rows, 4, QTableWidgetItem(str(row[4])))
                self.tableWidget8.setItem(rows, 5, QTableWidgetItem(str(row2[1])))
                self.tableWidget8.setItem(rows, 6, QTableWidgetItem(str(row[5])))
                self.tableWidget8.setItem(rows, 7, QTableWidgetItem(str(row2[2])))
                try:
                    sum_sum += row2[2]
                except:
                    break_sign = True
                    break
        self.tableWidget8.setRowCount(rows + 2)
        self.tableWidget8.setItem(rows + 1, 6, QTableWidgetItem('مجموع'))
        if break_sign is not True:
            self.tableWidget8.setItem(rows + 1, 7, QTableWidgetItem(str(sum_sum)))
        else:
            self.tableWidget8.setItem(rows + 1, 7, QTableWidgetItem('-----'))

        deli = InitialDelegate(2, self.tableWidget8)
        self.tableWidget8.setItemDelegateForColumn(6, deli)
        self.tableWidget8.setItemDelegateForColumn(7, deli)
        self.tableWidget8.resizeColumnsToContents()

    def new_project_box(self):
        window = save_and_new_boxes.SaveBox()
        window.setupUi(window)
        window.exec_()
        self.project_name = window.lineEdit.text()
        self.customer_name = window.lineEdit_2.text()
        table_name = self.project_name.replace(" ", "_")
        self.table1 = "_" + table_name + "_1"
        self.table2 = "_" + table_name + "_2"
        self.table3 = "_" + table_name + "_3"

        if self.project_name != "":
            cur = self.connection.cursor()
            cur.execute(
                f"INSERT INTO ProjectName (name, customer) VALUES ('{self.project_name}','{self.customer_name}')")
            cur.execute(f"CREATE TABLE '{self.table1}' (id  VARCHAR (40) REFERENCES equipment (id) PRIMARY KEY,pcs)")
            cur.execute(f"CREATE TABLE '{self.table2}' (id,pcs)")
            cur.execute(f"CREATE TABLE '{self.table3}' (id  REFERENCES equipment ,pcs,price_t)")
            self.connection.commit()
            self.load_data()

    def load_project_box(self):
        window = save_and_new_boxes.LoadBox()
        window.setupUi(window)
        window.exec_()
        if window.listWidget.count() != 0 or None:
            self.project_name = window.listWidget.currentItem().text()
            table_name = self.project_name.replace(" ", "_")
            self.table1 = "_" + table_name + "_1"
            self.table2 = "_" + table_name + "_2"
            self.table3 = "_" + table_name + "_3"
            if self.project_name != "":

                self.load_data()
        else:
            self.project_name = None
            self.label0.setText("")
            for i in range(1, 7):
                command1 = 'self.tableWidget' + str(i) + '.rowCount()'
                command2 = 'self.tableWidget' + str(i) + '.removeRow(0)'
                while eval(command1) > 0:
                    eval(command2)

    def new_combination_box(self):
        window = new_combination.combination_managment()
        window.setupUi(window)
        window.exec_()
        if self.project_name != None:
            self.load_data()

    def new_item_box(self):
        window = new_item.combination_managment()
        window.setupUi(window)
        window.exec_()
        if self.project_name != None:
            self.load_data()

    def result(self):
        try:
            cur = self.connection.cursor()
            cur1 = self.connection.cursor()
            cur2 = self.connection.cursor()
            cur3 = self.connection.cursor()
            cur4 = self.connection.cursor()

            cur.execute(f"DELETE FROM {self.table3}")
            self.connection.commit()

            for row in cur.execute(f"SELECT *FROM {self.table2}"):
                for row1 in cur1.execute(f"SELECT *FROM combination WHERE id = '{row[0]}'"):
                    sum = int(row1[5]) * int(row[1])
                    cur2.execute(f"INSERT INTO {self.table3} (id,pcs) VALUES ({row1[4]},{sum})")
                self.connection.commit()
            for row4 in cur.execute(f"SELECT *FROM {self.table1}"):
                cur3.execute(f"INSERT INTO {self.table3} (id,pcs) VALUES ({row4[0]},{row4[1]})")
                self.connection.commit()
                cur4.execute(f"select id, sum(pcs) as Total from {self.table3} group by id")
                self.connection.commit()
                self.refreshing_table7()
        except:
            QMessageBox.critical(None, 'خطا', 'پروژه ای انتخاب نشده است.')

    def total_price(self):
        try:
            cur = self.connection.cursor()
            cur1 = self.connection.cursor()
            cur2 = self.connection.cursor()
            self.inputting_item_pcs()
            # self.refreshing_table8()
            row = 0
            while self.tableWidget8.item(row, 0) is not None:
                id = self.tableWidget8.item(row, 0).text()
                price = self.tableWidget8.item(row, 6).text()

                cur2.execute(f"UPDATE equipment SET price='{price}' WHERE id = {id}")
                row += 1
            self.connection.commit()
            break_alarm = False
            r = 0
            for row in cur.execute(f"SELECT *FROM {self.table3}"):

                for row1 in cur1.execute(f"SELECT *FROM equipment WHERE id = '{row[0]}'"):
                    try:
                        r += 1
                        price_total = int(row[1]) * int(row1[5])
                        cur2.execute(f"UPDATE {self.table3} SET price_t={price_total} Where id = {row[0]}")
                    except:
                        # self.tabWidget.setCurrentIndex(1)
                        self.tableWidget8.selectRow(r)
                        QMessageBox.critical(None, "خطا",
                                             'قیمت به درستی وارد نشده است. میتوانید در همین صفحه قیمت را وارد و مجددا '
                                             'محاسبه را کلیک کنید. این قمیت در دیتابیس ذخیره می گردد.')
                        break_alarm = True
                        break
                if break_alarm:
                    break
            self.connection.commit()
            self.refreshing_table8()
        except:
            QMessageBox.critical(None, 'خطا', 'پروژه ای انتخاب نشده است.')

    def to_excel(self):
        table7 = self.tableWidget7
        table8 = self.tableWidget8
        window = excel_box.Window()
        window.setupui(window, table7, table8, self.project_name)
        window.exec_()

    def print(self):
        table7 = self.tableWidget7
        table8 = self.tableWidget8
        window = print_box.Window()
        window.setupui(window, table7, table8, self.project_name)
        window.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "لیست لوازم پروژه های آبی"))
        self.label.setText(
            _translate("MainWindow", "شیر آلات و یا مجموعه شیرآلاتی که در طرح استفاده می گردد را انتخاب کنید."))
        self.new_item.setText(_translate("MainWindow", "تعریف آیتم جدید"))
        self.new_component.setText(_translate("MainWindow", "تعریف مجموعه جدید"))
        self.lineEdit.setText(_translate("MainWindow", ""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "تعریف مجموعه "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "ورودی"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "لیست لوازم"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "لیست قیمت"))
        self.__file.setTitle(_translate("MainWindow", "فایل"))
        self.__about.setTitle(_translate("MainWindow", "درباره"))
        self.__tools.setTitle(_translate("MainWindow", "ابزار"))
        self.acrion_1.setText(_translate("MainWindow", "پروژه جدید"))
        self.acrion_1.setToolTip(_translate("MainWindow", "ایجاد پروژه جدید"))
        self.action_2.setText(_translate("MainWindow", "بارگزاری پروژه"))
        self.action_4.setText(_translate("MainWindow", "خروج"))
        self.action_5.setText(_translate("MainWindow", "درباره برنامه"))
        self.action_3.setText(_translate("MainWindow", "راهنما"))
        self.action_7.setText(_translate("MainWindow", "خروجی به اکسل"))

        self.action_9.setText(_translate("MainWindow", "مدیریت مجموعه ها"))
        self.action_10.setText(_translate("MainWindow", "مدیریت آیتم ها"))
        self.action_12.setText(_translate("MainWindow", "پرینت"))
        self.tabWidget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


