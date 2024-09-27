import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QVBoxLayout, QComboBox, QToolBar
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setWindowIcon(QIcon.fromTheme("system-search"))
        # self.setGeometry(370, 150, 640, 480)
        self.setMinimumSize(800,600)
        
        # Set the menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        search_menu_item = self.menuBar().addMenu("&Search")
        # Set action for the file menu
        add_student_action = QAction(QIcon("icons/add.png"),"Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)
        # Set action for the help menu
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        # Set action for the search menu
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search_student)
        search_menu_item.addAction(search_action)
        
        # Add table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        stylesheet = "::section{Background-color:rgb(240, 240, 240);border: .5px outset white;border-radius: 5px}"
        self.table.horizontalHeader().setStyleSheet(stylesheet)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        
        # Create toolbar and add toolbar element
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)
        
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
    
    def search_student(self):
        dialog = SearchDialog()
        dialog.exec()
        

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)
        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        # add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)
        # add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)     
        
        self.setLayout(layout)
        
    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(200)
        
        layout = QVBoxLayout()
        
        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)
        # Add a submit button
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)     
        
        self.setLayout(layout)
    
    def search_student(self):
        name = self.student_name.text()
        
        # connection = sqlite3.connect("database.db")
        # cursor = connection.cursor()
        # result = cursor.execute("SELECT * FROM students WHERE name=?", (name,))
        # rows = list(result)
        items = window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            window.table.item(item.row(), 1).setSelected(True)
        
        # cursor.close()
        # connection.close()
        


app = QApplication(sys.argv)
window = MainWindow()
window.load_data()
window.show()
sys.exit(app.exec())