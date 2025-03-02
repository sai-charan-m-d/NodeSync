from PySide6.QtWidgets import QApplication, QMainWindow 
from PySide6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        
        self.app = app
        self.setWindowTitle("NodeSync")
        self.icon = QIcon("icons/nodesync.png")
        self.setWindowIcon(self.icon)
