import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow
from PyQt6.QtGui import QIcon, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setWindowIcon(QIcon.fromTheme("system-search"))
        
        # Set the menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        # Set action for the file menu
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)
        # Set action for the help menu
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        
        
        
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())