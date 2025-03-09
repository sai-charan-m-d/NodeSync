from PySide6.QtWidgets import QTreeWidget, QTreeView, QTreeWidgetItem, QTreeWidgetItemIterator, QMenu
from PySide6.QtGui import QIcon,QAction
from PySide6.QtCore import Qt, QSettings
import os
import subprocess
import platform
import json

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.folder_icon = QIcon("NodeSync/icons/folder-48.png")
        self.file_icon = QIcon("NodeSync/icons/blender-48.png")
        self.file_icons = {
            ".blend": QIcon("NodeSync/icons/blender-48.png"),
            ".usd": QIcon("NodeSync/icons/usd-icon.png"),
            ".usdc": QIcon("NodeSync/icons/usd-icon.png"),
            ".jpg": QIcon("NodeSync/icons/jpeg-40.png"),
            ".png": QIcon("NodeSync/icons/png-48.png"),
            ".exr": QIcon("NodeSync/icons/exr-64.png"),
            ".json": QIcon("NodeSync/icons/json-48.png"),
            ".hiplc": QIcon("NodeSync/icons/sidefx_badge_flat.png"),
            ".hip": QIcon("NodeSync/icons/sidefx_badge_flat.png"),
            ".hipnc": QIcon("NodeSync/icons/sidefx_badge_flat.png"),
            "default": QIcon("icons/file.png")  #  Default file icon
        }
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def populate_tree(self, folder_path):
        """ Recursively populates the tree with folders & files."""
        self.clear()  #  Clear previous content

        root_item = QTreeWidgetItem(self, [os.path.basename(folder_path)])
        self.addTopLevelItem(root_item)
        self._populate_tree_recursive(root_item, folder_path)
        self.expandAll()  #  Expand tree for better visibility


    def _populate_tree_recursive(self, parent_widget, folder_path):
        """ Recursively loads all folders & files into the tree with custom icons."""
        for item_name in sorted(os.listdir(folder_path)):
            item_path = os.path.join(folder_path, item_name)
            tree_item = QTreeWidgetItem(parent_widget, [item_name])

            if os.path.isdir(item_path):  #  Folder
                tree_item.setIcon(0, self.folder_icon)
                self._populate_tree_recursive(tree_item, item_path)  #  Recursively add subfolders
            else:  # File
                file_extension = os.path.splitext(item_name)[1].lower()  #  Get file extension
                tree_item.setIcon(0, self.file_icons.get(file_extension, self.file_icons["default"]))  #  Set icon

    def show_context_menu(self, position):
        """ Right-click menu for folder actions."""
        item = self.itemAt(position)

        if item:
            menu = QMenu(self)
            open_action = QAction("Open", self)
            delete_action = QAction("Delete", self)

            menu.addAction(open_action)
            menu.addAction(delete_action)

            action = menu.exec_(self.viewport().mapToGlobal(position))

            if action == open_action:
                self.open_file(item)
            elif action == delete_action:
                self.delete_folder(item)

    def open_folder(self, item):
        """ Opens the selected folder in the system file explorer."""
        folder_path = self.get_item_path(item)
        if folder_path and os.path.exists(folder_path):
            if platform.system() == "Windows":
                subprocess.run(["explorer", folder_path], check=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", folder_path], check=True)
            else:  # Linux
                subprocess.run(["xdg-open", folder_path], check=True)
 
    def get_item_path(self, item):
        """ Constructs the correct absolute path without duplicating the project folder."""
        path_parts = []

        while item:
            path_parts.insert(0, item.text(0))
            item = item.parent()

        if not path_parts:
            print("Error: No item selected in the tree.")
            return None  #  Prevents returning an invalid path

        project_root = self.get_project_root()  #  Get the correct project path from metadata.json
        if not project_root:
            print("Error: No project selected or metadata missing!")
            return None  #  Prevents returning an invalid path

        #  Ensure project name is not duplicated
        path_without_project = os.path.join(*path_parts)
        if project_root.endswith(path_parts[0]):  
            path_without_project = os.path.join(*path_parts[1:])  #  Remove duplicate project folder

        full_path = os.path.join(project_root, path_without_project)
        return os.path.abspath(full_path)  #  Ensure absolute path

    def get_project_root(self):
        """ Returns the full project path by reading `metadata.json`."""
        main_window = self.window()  #  Get reference to MainWindow
        if hasattr(main_window, "project_list_widget"):
            selected_item = main_window.project_list_widget.currentItem()
            if selected_item:
                project_path = selected_item.data(100)  #  Get absolute project path
                metadata_file = os.path.join(project_path, "metadata.json")

                if os.path.exists(metadata_file):
                    try:
                        with open(metadata_file, "r") as f:
                            metadata = json.load(f)
                            return metadata.get("path", project_path)  #  Use path from metadata
                    except json.JSONDecodeError:
                        print(f"Error: Could not read metadata.json at {metadata_file}")

                return project_path  #  Fallback if metadata is missing
        return None  #  Return `None` instead of an empty string

    def delete_folder(self, item):
        """ Deletes the selected folder (not implemented to prevent accidental deletion)."""
        print(f"Delete folder: {self.get_item_path(item)}")

    def launch_blender(self, file_path):
        """ Launches Blender using the saved path from settings."""
        settings = QSettings("NodeSync", "Config")
        blender_executable = settings.value("blender_path", "blender")  #  Load from settings

        if not os.path.exists(blender_executable) and blender_executable != "blender":
            print(f"Error: Blender executable not found at {blender_executable}")
            return

        try:
            print(f"Debug: Opening Blender using {blender_executable}")
            subprocess.run([blender_executable, file_path], check=True)
        except Exception as e:
            print(f"Error launching Blender: {e}")

    def is_blender_available(self):
        """ Checks if Blender is available in system PATH."""
        try:
            subprocess.run(["blender", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except FileNotFoundError:
            return False


    def open_file(self, item):
        """ Opens the selected file. Launches Blender if it's a `.blend` file."""
        file_path = self.get_item_path(item)

        if not file_path:
            print("Error: Could not determine file path!")
            return

        print(f"Debug: Attempting to open file - {file_path}")  #  Debugging output

        if not os.path.exists(file_path):
            print(f"Error: File not found - {file_path}")
            return

        if file_path.endswith(".blend"):
            self.launch_blender(file_path)
        else:
            self.open_with_default_app(file_path)

    def open_with_default_app(self, file_path):
        """ Opens non-`.blend` files with the system's default application."""
        try:
            if platform.system() == "Windows":
                os.startfile(file_path)  #  Windows
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path], check=True)
            else:  # Linux
                subprocess.run(["xdg-open", file_path], check=True)
        except Exception as e:
            print(f"Error opening file: {e}")