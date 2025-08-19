import os
from functions.get_files_info import get_files_info_internal

def write_file(working_directory, file_path, content):
    if f"Error: Cannot list \"{file_path}\" as it is outside the permitted working directory" in get_files_info_internal(working_directory, file_path):
        return f"Error: Cannot list \"{file_path}\" as it is outside the permitted working directory"
    # return get_files_info(working_directory, file_path)
    path = os.path.join(working_directory, file_path)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except Exception as e:
        return f"Error: {e}"

    try:
        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
