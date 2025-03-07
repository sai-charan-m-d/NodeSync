import os
from pathlib import Path

def folder_exists(folder_path):
    return os.path.exits(folder_path) and os.path.isdir(folder_path)

def project_exists(project_name, project_folder):
    if project_name in project_folder:
        return True
    else:
        return False

def folder_name_exists(folder_name:str, parent_dir_path:str):
    path = Path(parent_dir_path) / folder_name
    
    if path.exists():
        return True
    else:
        return False