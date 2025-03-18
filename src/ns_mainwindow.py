from PySide6.QtWidgets import QApplication, QMainWindow , QStatusBar
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt
from src.ns_create_project_window import CreateProjectWindow
from src.ns_list_widget import ProjectListWidget
from src.ns_settings_window import SettingsWindowWidget

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
        self.project_list_widget = ProjectListWidget()
        self.setCentralWidget(self.project_list_widget)

        #creating the menu bar
        menubar = self.menuBar()

        #File Menu 
        file_menu = menubar.addMenu("&File")

        #Actions in the File Menu
        create_project_action = file_menu.addAction("New Project")
        create_project_action.triggered.connect(self.create_project_launch)
        #create_project_action.toolTip("Create's a new project and adds it to the list")
        load_project_action = file_menu.addAction("Load Project")
        file_menu.addSeparator()

        #Quit App
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)

        #Settings Menu
        settings_menu = menubar.addMenu("&Settings")
        create_settings_action = settings_menu.addAction("settings")
        create_settings_action.triggered.connect(self.settings_launch)

        #statusBar
        self.setStatusBar(QStatusBar(self))

    def quit_app(self):
        self.app.quit()
    
    def create_project_launch(self):
        self.widget = CreateProjectWindow(self, self.project_list_widget)
        self.widget.show()
        
    def list_widget(self):
        self.widget = ProjectListWidget()
        self.widget.show()

    def settings_launch(self):
        self.widget = SettingsWindowWidget()
        self.widget.show()

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
