import os
import subprocess
from functions.get_files_info import get_files_info
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file inside the working directory with optional arguments. Captures stdout, stderr, exit code, and enforces a 30-second timeout.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path (from the working directory) to the Python file to execute. Must end with .py.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of string arguments to pass to the Python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single command-line argument string",
                ),
            ),
        },
        required=["file_path"],
    ),
)


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