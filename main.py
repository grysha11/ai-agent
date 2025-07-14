import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
        contents=messages
    )
    metadata = response.usage_metadata
    print(response.text)
    if verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
