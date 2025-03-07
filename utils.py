import os, json, datetime
from pathlib import Path

def folder_exists(folder_path):
    return os.path.exits(folder_path) and os.path.isdir(folder_path)

def project_exists(project_name, project_folder):
    if project_name in project_folder:
        return True
    else:
        return False

def folder_name_exists(folder_name:str, parent_dir_path:str):
    path = Path(parent_dir_path+'/'+folder_name)
    
    if path.exists():
        return True
    else:
        return False

PROJECTS_FILE = "projects.json"  #  Store project list in JSON

def get_folder_structure(directory):
    """ Recursively gets all subfolders in a directory and saves them properly."""
    folder_structure = {}

    for root, dirs, _ in os.walk(directory):  
        relative_path = os.path.relpath(root, directory)

        #  Store subfolders properly, ensuring they map to the right folder
        if relative_path == ".":
            folder_structure["."] = dirs  # ✅ Root folders
        else:
            folder_structure[relative_path] = dirs  # ✅ Subfolders

    return folder_structure

def generate_metadata(project_name, project_path):
    """ Generates and saves project metadata, including all subfolders."""
    folder_structure = get_folder_structure(project_path)  

    metadata = {
        "name": project_name,
        "path": project_path,
        "created_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "folders": folder_structure  
    }

    metadata_file = os.path.join(project_path, "metadata.json")
    
    try:
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)
        return metadata  
    except Exception as e:
        print(f"Error writing metadata file: {e}")
        return None  

def save_project_list(metadata):
    """ Saves project metadata to a JSON file for persistence."""
    projects = []

    #  Load existing projects if the file exists
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, "r") as f:
            try:
                projects = json.load(f)
            except json.JSONDecodeError:
                projects = []  # Handle corrupted JSON

    #  Prevent duplicates
    if not any(p["path"] == metadata["path"] for p in projects):
        projects.append(metadata)

    #  Save the updated project list
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f, indent=4)

def load_project_list():
    """ Loads project metadata from JSON and returns a list."""
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Error: Could not decode projects.json")
                return []
    return []
