from PySide6.QtWidgets import QApplication, QMainWindow , QStatusBar
from PySide6.QtGui import QIcon, QAction
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
        central_widget = ProjectListWidget()
        self.setCentralWidget(central_widget)

        #creating the menu bar
        menubar = self.menuBar()

        #File Menu 
        file_menu = menubar.addMenu("&File")
        #Actions in the File Menu
        create_project_action = file_menu.addAction("New Project")
        create_project_action.triggered.connect(self.create_project_launch)
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
        self.widget = CreateProjectWindow()
        self.widget.show()
        
    def list_widget(self):
        self.widget = ProjectListWidget()
        self.widget.show()

    def settings_launch(self):
        self.widget = SettingsWindowWidget()
        self.widget.show()