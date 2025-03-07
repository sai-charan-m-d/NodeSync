from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QFileDialog,QPushButton,QLineEdit,QHBoxLayout,QTextEdit,QMessageBox,QGraphicsDropShadowEffect,QListWidgetItem
from PySide6.QtCore import Qt, QSettings,QPoint
from PySide6.QtGui import QCursor, QColor
from utils import folder_name_exists, generate_metadata, save_project_list
import os
import json

class CreateProjectWindow(QWidget):
    def __init__(self, main_window=None, project_list_widget = None):
        super().__init__()
        self.main_window = main_window
        self.project_list_widget = project_list_widget
        self.settings = QSettings("NodeSync", "Config")
        self.offset = QPoint()
        self.initUI()
        self.center_within_main()
        
    def initUI(self):
        self.setWindowTitle("Create Project")
        self.setGeometry(150,150,500,200)
        self.setWindowFlag(Qt.FramelessWindowHint)

        default_project_dir = self.settings.value("project_dir", "")

        #Project Name Layout
        project_name_layout = QHBoxLayout()
        project_name_label = QLabel("Project Name")
        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("Name of the Project")
        self.project_name.textChanged.connect(self.disable_create_button)
        project_name_layout.addWidget(project_name_label)
        project_name_layout.addWidget(self.project_name)

        #Project Location Layout
        project_location_layout = QHBoxLayout()
        project_location_label = QLabel("Project Location")
        self.project_location_textbox = QLineEdit()
        self.project_location_textbox.setText(default_project_dir)
        self.project_location_textbox.textChanged.connect(self.disable_create_button)
    
        project_location_browser = QPushButton("Browse")
        project_location_browser.clicked.connect(self.choose_dir)
        project_location_layout.addWidget(project_location_label)
        project_location_layout.addWidget(self.project_location_textbox)
        project_location_layout.addWidget(project_location_browser)

        #Button Layout
        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Create Project")

        # Create Button Tool Tip
        if self.project_exists:
            self.create_button.setToolTip("Creates the folder structure")
        else:
            self.create_button.setToolTip("Creates the folder structure")

        cancel_button = QPushButton("Cancel")
        cancel_button.setToolTip("Cancel the Folder Creation")
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(cancel_button)
        self.create_button.clicked.connect(self.create_project_folders)
        cancel_button.clicked.connect(self.quit_widget)
 
        v_layout = QVBoxLayout()
        v_layout.addLayout(project_name_layout)
        v_layout.addLayout(project_location_layout)
        v_layout.addLayout(button_layout)

        self.setLayout(v_layout)
        self.disable_create_button()
        self.show()
    
    def center_within_main(self):
        if self.main_window:
            main_geometry = self.main_window.geometry()
            new_x = main_geometry.x() + (main_geometry.width() - self.width()) // 2 
            new_y = main_geometry.y() + (main_geometry.height() - self.height()) // 2
            self.move(QPoint(new_x,new_y))

    def choose_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select the Directory")
        if dir_path:
            self.project_location_textbox.setText(str(dir_path))

    def load_folder_structure(self):
        
        try:
            with open("NodeSync/folder_structure.json", "r") as f:
                return json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load folder structure:\n{e}")
            return {}

    def create_project_folders(self):
        """ Creates the project folders and predefined subfolders, then saves metadata."""
        dir_path = self.project_location_textbox.text().strip()
        project_name_text = self.project_name.text().strip()

        if not dir_path:
            QMessageBox.warning(self, "Error", "No Directory Selected")
            return

        project_folder = os.path.join(dir_path, project_name_text)

        try:
            os.makedirs(project_folder, exist_ok=True)

            #  Load predefined folder structure from JSON
            folder_structure = self.load_folder_structure()

            #  Create folders & subfolders dynamically
            for main_folder, sub_folders in folder_structure.items():
                main_folder_path = os.path.join(project_folder, main_folder)
                os.makedirs(main_folder_path, exist_ok=True)

                for sub_folder in sub_folders:
                    sub_folder_path = os.path.join(main_folder_path, sub_folder)
                    os.makedirs(sub_folder_path, exist_ok=True)  # ✅ Create subfolders properly

            #  Generate metadata with full folder structure
            metadata = generate_metadata(project_name_text, project_folder)

            if metadata:
                QMessageBox.information(self, "Success", f"Project Created at:\n{project_folder}")
                self.add_project_to_list(metadata)
            else:
                QMessageBox.warning(self, "Error", "Failed to create metadata.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create folders:\n{e}")

        self.close()

    def quit_widget(self):
        QMessageBox.information(self, "Cancelled", "Project creation cancelled")
        self.close()

    def project_exists(self):
        proj_name = self.project_name.text().strip()
        proj_path = self.project_location_textbox.text().strip()

        return folder_name_exists(proj_name, proj_path)

    def disable_create_button(self):
        if self.project_exists():
            self.create_button.setEnabled(False)
            self.create_button.setCursor(QCursor(Qt.ForbiddenCursor))
        else:
            self.create_button.setEnabled(True)
            self.create_button.setCursor(QCursor(Qt.PointingHandCursor))

    # Mouse Events to move the Widget
    def mousePressEvent(self, event):
        """Detects mouse click and stores the offset."""
        if event.button() == Qt.LeftButton:
            self.dragging = True  
            self.offset = event.globalPosition().toPoint() - self.pos() 
            event.accept()

    def mouseMoveEvent(self, event):
        """Moves the window while dragging."""
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.offset) 
            event.accept()

    def mouseReleaseEvent(self, event):
        """Stops dragging when mouse button is released."""
        if event.button() == Qt.LeftButton:
            self.dragging = False 
            event.accept()

    def add_project_to_list(self, metadata):
        """ Adds a new project to QListWidget using metadata."""
        if self.project_list_widget:
            item = QListWidgetItem(metadata["name"])
            item.setData(100, metadata["path"])  #  Store project path in metadata
            self.project_list_widget.addItem(item)
            save_project_list(metadata)