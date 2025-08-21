import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python_file, run_python_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file content
- Create or overwrite a file
- Execute a Python file with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

function_names = {
    "get_files_info" : get_files_info,
    "get_file_content" : get_file_content,
    "write_file" : write_file,
    "run_python_file" : run_python_file,
}

def main():
    if len(sys.argv) < 2:
        print("Error: Incorrect amount of arguments\t Usage: uv main.py \"prompt\"")
        sys.exit(1)
    client = init_gemini()
    user_prompt = sys.argv[1]
    verbose = False
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    if len(sys.argv) == 3:
        if sys.argv[2] == "--verbose":
            verbose = True
        else:
            print("Error: Incorrect amount of arguments\t Usage: uv main.py \"prompt\"")
            sys.exit(1)
    generate_response(client, user_prompt, verbose)

def init_gemini():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    return client

def generate_response(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    metadata = response.usage_metadata
    if response.function_calls:
        function_calls = response.function_calls
        for function_call_part in function_calls:
            res = call_function(function_call_part, verbose)
            if not res.parts[0].function_response.response:
                raise RuntimeError("Fatal: no respose on function call.")
            if verbose:
                print(f"-> {res.parts[0].function_response.response}")
    else:
        print(response.text)
    if verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")

def call_function(function_call_part, verbose=False):
    if function_call_part.name not in function_names:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = "calculator"
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f" - Calling function: {function_call_part.name}")
    result = function_names[function_call_part.name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )

if __name__ == "__main__":
    main()
