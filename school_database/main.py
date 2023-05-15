from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton,\
    QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Member Management System")

        # Menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        add_menu_item = self.menuBar().addMenu("&Help")

        add_member_action = QAction("Add Member", self)
        add_member_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_member_action)

        search_member_action = QAction("Search for a member", self)
        search_member_action.triggered.connect(self.start_search)
        file_menu_item.addAction(search_member_action)

        about_action = QAction("About", self)
        add_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole) # For Macs

        # Table

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("id", "Name", "Course", "Email", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):

        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)

            for column_number, data in enumerate(row_data):

                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def start_search(self):
        s = SearchFunction()
        s.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Set a new Member")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.member_name = QLineEdit()
        self.member_name.setPlaceholderText("Name")
        layout.addWidget(self.member_name)

        self.course = QComboBox()
        courses = ["None", "Python", "C++", "Japanese", "2D Art", "3D Art"]
        self.course.addItems(courses)
        layout.addWidget(self.course)

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Email")
        layout.addWidget(self.phone)

        button = QPushButton("Submit")
        button.clicked.connect(self.add_member)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_member(self):
        n = self.member_name.text()
        c = self.course.itemText(self.course.currentIndex())
        p = self.phone.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (n, c, p))
        connection.commit()
        cursor.close()
        connection.close()
        MainRecords.load_data()
        self.close()

class SearchFunction(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search for a member")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by name")

        layout.addWidget(self.search_box)

        confirm_button = QPushButton("Search")

        layout.addWidget(confirm_button)

        self.setLayout(layout)


app = QApplication(sys.argv)
MainRecords = MainWindow()
MainRecords.show()
MainRecords.load_data()
sys.exit(app.exec())