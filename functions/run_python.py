import os
import subprocess
from functions.get_files_info import get_files_info

def run_python_file(working_directory, file_path, args=[]):
    if f"Error: Cannot list \"{file_path}\" as it is outside the permitted working directory" in get_files_info(working_directory, file_path):
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    path = os.path.join(working_directory, file_path)
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'
    if not path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    cmd = ["python3", path] + args
    try:
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        res = ""
        if not process.stdout and not process.stderr:
            res += "No output produced\n"
        res += f"STDOUT: {process.stdout}\n"
        res += f"STDERR: {process.stderr}\n"
        if process.returncode != 0:
            res += f"Process exited with code {process.returncode}\n"
        res.strip()
    except subprocess.TimeoutExpired as e:
        return f"Error: Process timed out after 30 seconds.\nPartial STDOUT: {e.stdout}\nPartial STDERR: {e.stderr}"
    except Exception as e:
        return f"Error: {e}"
    
    return res