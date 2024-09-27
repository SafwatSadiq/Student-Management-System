import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt


class DataBaseConnection:
    def __init__(self, database_file='database.db'):
        self.database_file = database_file
        
    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection


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
        about_action.triggered.connect(self.about)
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
        
        # Create toolbar and add toolbar element
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # Detect cell click
        self.table.cellClicked.connect(self.cell_clicked)
        
    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)
        
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)
              
    def load_data(self):
        connection = DataBaseConnection().connect()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()
         
    def edit(self):
        dialog = EditDialog()
        dialog.exec()
    
    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()
    
    def about(self):   
        dialog = AboutDialog()
        dialog.exec()
        
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
    
    def search_student(self):
        dialog = SearchDialog()
        dialog.exec()
        

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")  
        content = """
Student Management System
----------------------------------------------------------------
Version - 1.0
----------------------------------------------------------------
    This app was created by Safwat Sadiq during a course.
    Feel Free to modify it!
----------------------------------------------------------------
        """
        self.setText(content)
        self.setWindowIcon(QIcon.fromTheme("help-about"))


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(200)
        
        layout = QVBoxLayout()
        
        index = window.table.currentRow()
        
        # Get id from selected row
        self.student_id = window.table.item(index, 0).text()
        # Add student name widget
        student_name = window.table.item(index, 1).text()
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)
        
        # Add combo box of courses
        course_name = window.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)
        
        # add mobile widget
        mobile = window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)
        
        # add a submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)     
        
        self.setLayout(layout)
        
    def update_student(self):
        connection = DataBaseConnection().connect()
        cursor = connection.cursor()
        
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(), 
                        self.course_name.itemText(self.course_name.currentIndex()), 
                        self.mobile.text(), 
                        self.student_id))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        window.load_data()
    

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        self.setFixedWidth(220)
        self.setFixedHeight(90)
        
        layout = QGridLayout()
        
        confirmation = QLabel("Are you sure you want to delete?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")
        
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1,0)
        layout.addWidget(no_button, 1, 1)
        
        yes_button.clicked.connect(self.delete_student)
        
        self.setLayout(layout)
    
    def delete_student(self):
        index = window.table.currentRow()
        # Get id from selected row
        self.student_id = window.table.item(index, 0).text()
        
        connection = DataBaseConnection().connect()
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM students WHERE id = ?", (self.student_id, ))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        window.load_data()
        
        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Record was deleted successfull!")
        confirmation_widget.exec()


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
        
        connection = DataBaseConnection().connect()
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
        
        # connection = DataBaseConnection().connect()
        # cursor = connection.cursor()
        # result = cursor.execute("SELECT * FROM students WHERE name=?", (name,))
        # rows = list(result)
        items = window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            window.table.item(item.row(), 1).setSelected(True)
        
        # cursor.close()
        # connection.close()
        

app = QApplication(sys.argv)
window = MainWindow()
window.load_data()
window.show()
sys.exit(app.exec())