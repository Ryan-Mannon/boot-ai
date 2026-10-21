import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()


    messages = [
        {"role": "user", "content": args.user_prompt},
    ]

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    #Error handling
    if api_key == None:
        raise RuntimeError("key not found")
    if response.usage == None:
        raise RuntimeError("usage can't be None. Failed API request")


    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print(response.choices[0].message.content)



if __name__ == "__main__":
    main()
