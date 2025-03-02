from PySide6.QtWidgets import QApplication, QMainWindow , QStatusBar
from PySide6.QtGui import QIcon, QAction

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.setWindowTitle("NodeSync")
        self.icon = QIcon("icons/nodesync.png")
        self.setWindowIcon(self.icon)
        
        width = 800
        height = 600
        self.setMinimumSize(width, height)

        #creating the menu bar
        menubar = self.menuBar()

        #File Menu 
        file_menu = menubar.addMenu("&File")
        #Actions in the File Menu
        create_project_action = file_menu.addAction("New Project")
        load_project_action = file_menu.addAction("Load Project")
        file_menu.addSeparator()

        #Quit App
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)

        #statusBar
        self.setStatusBar(QStatusBar(self))

    def quit_app(self):
        self.app.quit()