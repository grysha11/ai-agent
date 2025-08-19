from functions.get_files_info import get_files_info_internal
from config import MAX_FILE_SIZE
from google.genai import types
import os

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contets of a file in the specified file path, contrained to the working_directory. Will return Error if the file is missing, is a directory, or outside of working directory. Large files are truncated to 10,000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path (from the working directory) to the file to be read.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    if f"Error: Cannot list \"{file_path}\" as it is outside the permitted working directory" in get_files_info_internal(working_directory, file_path):
        return f"Error: Cannot list \"{file_path}\" as it is outside the permitted working directory"
    if "is_dir=True" in get_files_info_internal(working_directory, file_path) or len(get_files_info_internal(working_directory, file_path)) == 0:
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