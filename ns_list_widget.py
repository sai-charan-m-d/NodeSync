from PySide6.QtWidgets import QApplication, QListWidget, QListView, QListWidgetItem
from PySide6.QtCore import Qt

class ProjectListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projects")