from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QFileDialog,QPushButton,QLineEdit,QHBoxLayout,QTextEdit
from PySide6.QtCore import Qt
import os
#from PySide6.QtCore import 
#from PySide6.QtGui import

class CreateProjectWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(100,100,800,600)
        self.setWindowTitle("Create Project")
        self.setGeometry(150,150,500,200)
        self.setWindowFlag(Qt.FramelessWindowHint)

        #Project Name Layout
        project_name_layout = QHBoxLayout()
        project_name_label = QLabel("Project Name")
        project_name = QLineEdit()
        project_name_layout.addWidget(project_name_label)
        project_name_layout.addWidget(project_name)

        #Project Location Layout
        project_location_layout = QHBoxLayout()
        project_location_label = QLabel("Project Location")
        self.project_location_textbox = QLineEdit()
        project_location_browser = QPushButton("Browse")
        project_location_browser.clicked.connect(self.choose_dir)
        project_location_layout.addWidget(project_location_label)
        project_location_layout.addWidget(self.project_location_textbox)
        project_location_layout.addWidget(project_location_browser)

        #Button Layout
        button_layout = QHBoxLayout()
        create_button = QPushButton("Create Project")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(create_button)
        button_layout.addWidget(cancel_button)
        create_button.clicked.connect(self.create_project_folders)
        cancel_button.clicked.connect(self.quit_widget)


        v_layout = QVBoxLayout()
        v_layout.addLayout(project_name_layout)
        v_layout.addLayout(project_location_layout)
        v_layout.addLayout(button_layout)

        self.setLayout(v_layout)
        self.show()
    
    def choose_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select the Directory")
        self.project_location_textbox.setText(str(dir_path))
    
    def create_project_folders(self):
        dir_path = self.project_location_textbox.text()
        os.path.join(dir_path)
        print(os.getcwd())
    
    def quit_widget(self):
        self.close()
