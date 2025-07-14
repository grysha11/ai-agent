import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    client = init_gemini()
    if len(sys.argv) < 2:
        print("Error: Incorrect amount of arguments\t Usage: uv main.py \"prompt\"")
        sys.exit(1)
    args = sys.argv[1:]
    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    generate_response(client, user_prompt)

def init_gemini():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    return client

def generate_response(client, messages):
    responce = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )
    metadata = responce.usage_metadata
    print(responce.text)
    print(f"Prompt tokens: {metadata.prompt_token_count}")
    print(f"Response tokens: {metadata.candidates_token_count}")




if __name__ == "__main__":
    main()
