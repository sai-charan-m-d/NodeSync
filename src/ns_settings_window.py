from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog
from PySide6.QtCore import QSettings

class SettingsWindowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.settings = QSettings("NodeSync", "Config")

        #  Project Directory Settings
        self.project_label = QLabel("Default Project Directory")
        self.project_dir_text = QLineEdit()
        self.project_browse = QPushButton("Browse")
        self.project_dir_text.setText(self.settings.value("project_dir", ""))
        self.project_browse.clicked.connect(self.load_project_folder)

        #  Blender Path Settings
        self.blender_label = QLabel("Blender Executable Path")
        self.blender_path_text = QLineEdit()
        self.blender_browse = QPushButton("Browse")
        self.blender_path_text.setText(self.settings.value("blender_path", ""))
        self.blender_browse.clicked.connect(self.load_blender_executable)

        #  Save Button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)

        #  Layouts
        layout = QVBoxLayout()

        # 🔹 Project Directory Section
        project_layout = QHBoxLayout()
        project_layout.addWidget(self.project_label)
        project_layout.addWidget(self.project_dir_text)
        project_layout.addWidget(self.project_browse)
        layout.addLayout(project_layout)

        # 🔹 Blender Path Section
        blender_layout = QHBoxLayout()
        blender_layout.addWidget(self.blender_label)
        blender_layout.addWidget(self.blender_path_text)
        blender_layout.addWidget(self.blender_browse)
        layout.addLayout(blender_layout)

        # 🔹 Save Button
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_settings(self):
        """ Saves project directory and Blender path settings."""
        self.settings.setValue("project_dir", self.project_dir_text.text())
        self.settings.setValue("blender_path", self.blender_path_text.text())
        self.close()

    def load_project_folder(self):
        """ Opens a file dialog to select the default project directory."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Master Folder")
        if dir_path:
            self.project_dir_text.setText(str(dir_path))

    def load_blender_executable(self):
        """ Opens a file dialog to select the Blender executable."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Blender Executable", "", "Executable Files (*.exe);;All Files (*)")
        if file_path:
            self.blender_path_text.setText(file_path)
