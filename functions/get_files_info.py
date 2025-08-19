import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    init_list = get_files_info_internal(working_directory, directory)
    res_str = ""

    for str in init_list:
        res_str += str + "\n"

    res_str = res_str.strip()
    return res_str

def get_files_info_internal(working_directory, directory=None):
    info = get_files_infos(working_directory, directory)
    res = list()
    if "Error" in info:
        res.append(f"Error: {info["Error"]}")
    else:
        for file, metadata in info.items():
            if "Error" in metadata:
                res.append(f"{file}: {metadata['Error']}")
            else:
                res.append(f"{file}: file_size={metadata['file_size']} bytes, is_dir={metadata['is_dir']}")
    return res

def get_files_infos(working_directory, directory=None):
    res = {}

    try:
        if directory.startswith("..") or directory.startswith("/"):
            return {"Error": f"Cannot list \"{directory}\" as it is outside the permitted working directory"}
        
        full_dir = os.path.join(working_directory, directory)

        if not os.path.isdir(full_dir) and not os.path.isfile(full_dir):
                return {"Error": f"No such file as \"{directory}\""}

        contents = os.listdir(full_dir)
        for content in contents:
            content_path = os.path.join(full_dir, content)
            try:
                res[content] = {
                    "file_size": os.path.getsize(content_path),
                    "is_dir": os.path.isdir(content_path)
                }
            except Exception as e:
                res[content] = {"Error": str(e)}
        return res
    except Exception as e:
        return {"Error": str(e)}
