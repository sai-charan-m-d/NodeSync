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

def generate_meta_data(project_name, project_path, folder_structure):
    metadata = {
        "name" : project_name,
        "path" : project_path,
        "created_date" : datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"),
        "folders": list(folder_structure.keys())

    }
    metadata_file = os.path.join(project_path,"metadata.json")

    try:
        with open(metadata_file, "w") as f:
            json.dump(metadata,f,indent=4)
        return metadata
    except Exception as e:
        print(f"Error writing metadata file : {e}")
        return None