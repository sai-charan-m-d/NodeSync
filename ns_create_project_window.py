from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QFileDialog,QPushButton,QLineEdit,QHBoxLayout
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

        #Project Name Layout
        project_name_layout = QHBoxLayout()
        project_name_label = QLabel("Project Name")
        project_name = QLineEdit()
        project_name_layout.addWidget(project_name_label)
        project_name_layout.addWidget(project_name)

        #Project Location Layout
        project_location_layout = QHBoxLayout()
        project_location_label = QLabel("Project Location")
        project_location_browser = QFileDialog()
        project_location_layout.addWidget(project_location_label)
        project_location_layout.addWidget(project_location_browser)

        #Button Layout
        button_layout = QHBoxLayout()
        create_button = QPushButton("Create Project")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(create_button)
        button_layout.addWidget(cancel_button)


        v_layout = QVBoxLayout()
        v_layout.addLayout(project_name_layout)
        v_layout.addLayout(project_location_layout)
        v_layout.addLayout(button_layout)

        self.setLayout(v_layout)
        self.show()
    
    def open_file(self):
        pass
