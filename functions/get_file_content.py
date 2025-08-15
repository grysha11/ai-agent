from functions.get_files_info import get_files_info
from config import MAX_FILE_SIZE
import os

def get_file_content(working_directory, file_path):
    if f"Error: Cannot list {file_path} as it is outside the permitted working directory" in get_files_info(working_directory, file_path):
        return f"Error: Cannot list {file_path} as it is outside the permitted working directory"
    if "is_dir=True" in get_files_info(working_directory, file_path) or len(get_files_info(working_directory, file_path)) == 0:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    path = os.path.join(working_directory, file_path)
    try:
        with open(path, "r") as f:
            file_content = f.read(MAX_FILE_SIZE)
        if os.path.getsize(path) > 1000:
            file_content += f'\nFile "{path}" truncated at 10000 characters'
        return file_content
    except Exception as e:
        return f"Error: {e}"