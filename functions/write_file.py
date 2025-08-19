import os
from functions.get_files_info import get_files_info_internal
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates or overwrites a file inside the working directory with the given content. Automatically creates parent directories if needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path (from the working directory) to the file where content should be written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

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
