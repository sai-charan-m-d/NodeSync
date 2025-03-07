from PySide6.QtWidgets import QApplication, QMainWindow , QStatusBar,QListWidgetItem,QHBoxLayout,QVBoxLayout,QWidget,QTreeWidgetItem
from PySide6.QtGui import QIcon, QAction
from src.ns_create_project_window import CreateProjectWindow
from src.ns_list_widget import ProjectListWidget
from src.ns_settings_window import SettingsWindowWidget
from src.ns_tree_widget import TreeWidget
import json
import os
from utils import load_project_list

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

        #List Widget
        self.project_list_widget = ProjectListWidget()
        self.project_list_widget.itemSelectionChanged.connect(self.load_project_tree)
        #Tree Widget
        self.project_tree_widget = TreeWidget()

        #Layout 
        layout = QHBoxLayout()
        layout.addWidget(self.project_list_widget)
        layout.addWidget(self.project_tree_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
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
        self.load_project_list()

    def quit_app(self):
        self.app.quit()
    
    def create_project_launch(self):
        self.widget = CreateProjectWindow(self,self.project_list_widget)
        self.widget.show()
        
    def list_widget(self):
        self.widget = ProjectListWidget()
        self.widget.show()

    def settings_launch(self):
        self.widget = SettingsWindowWidget()
        self.widget.show()

    def load_project_list(self):
        """ Loads saved projects and displays metadata in `QListWidget`."""
        projects = load_project_list()

        for project in projects:
            item = QListWidgetItem(project["name"])  #  Display project name
            item.setData(100, project["path"])  #  Store project path

            metadata = project.get("metadata", {})
            if metadata:
                created_date = metadata.get("created_date", "Unknown Date")
                item.setToolTip(f"📂 Path: {project['path']}\n📅 Created: {created_date}")

            self.project_list_widget.addItem(item)
    def load_project_tree(self):
        """ Loads the selected project's folder structure into the tree."""
        selected_item = self.project_list_widget.currentItem()

        if selected_item:
            project_path = selected_item.data(100)  #  Get stored path
            if os.path.exists(project_path):
                self.project_tree_widget.populate_tree(project_path)  #  