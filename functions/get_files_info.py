import os

def print_file_info(info):
    if "Error" in info:
        print(f"Error: {info["Error"]}")
    else:
        for file, metadata in info.items():
            if "Error" in metadata:
                print(f"{file}: {metadata['Error']}")
            else:
                print(f"{file}: file_size={metadata['file_size']} bytes, is_dir={metadata['is_dir']}")

def get_files_info(working_directory, directory=None):
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
