from PySide6.QtWidgets import QApplication, QMainWindow , QStatusBar, QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout,QVBoxLayout, QFileDialog
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QSettings
from src.ns_create_project_window import CreateProjectWindow
from src.ns_list_widget import ProjectListWidget

class SettingsWindowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")

        self.settings = QSettings("Project Directory")

        self.proj_dir = QLabel("Default Project Directory")
        self.proj_dir_label = QLineEdit()
        self.browse = QPushButton("Browse")
        self.proj_dir_label.setText(self.settings.value("project_dir",""))
        self.browse.clicked.connect(self.load_folder)

        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout = QHBoxLayout()
        layout.addWidget(self.proj_dir)
        v_layout = QVBoxLayout()
        layout.addWidget(self.proj_dir_label)
        layout.addWidget(self.browse)
        v_layout.addLayout(layout)
        v_layout.addWidget(save_button)
        self.setLayout(v_layout)

    def save_settings(self):
        self.settings.setValue("project_dir",self.proj_dir_label.text())
        self.close()
    def load_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Master Folder")
        self.proj_dir_label.setText(str(dir_path))