from PySide6.QtWidgets import QApplication, QMainWindow , QStatusBar, QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout,QVBoxLayout, QFileDialog
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QSettings
from ns_create_project_window import CreateProjectWindow
from ns_list_widget import ProjectListWidget

class SettingsWindowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")

        self.settings = QSettings("Project Directory")

        self.label = QLabel("Default Project Directory")
        self.label_text = QLineEdit()
        self.browse = QPushButton("Browse")
        self.label_text.setText(self.settings.value("project_dir",""))
        self.browse.clicked.connect(self.load_folder)

        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        v_layout = QVBoxLayout()
        layout.addWidget(self.label_text)
        layout.addWidget(self.browse)
        v_layout.addLayout(layout)
        v_layout.addWidget(save_button)
        self.setLayout(v_layout)

    def save_settings(self):
        self.settings.setValue("project_dir",self.label_text.text())
        self.close()
    def load_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Master Folder")
        self.label_text.setText(str(dir_path))