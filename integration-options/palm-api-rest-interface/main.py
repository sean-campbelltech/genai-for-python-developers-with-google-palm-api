# Step 1: pip3 install -r requirements.txt
# Step 2: Create .env file and add MODEL and API_KEY env variables

from dotenv import load_dotenv
import requests
import json
import os


def main():
    load_dotenv()

    API_KEY = os.getenv("PALM_API_KEY")
    MODEL_ID = os.getenv("MODEL_ID")

    api_url = f"https://generativelanguage.googleapis.com/v1beta3/models/{MODEL_ID}:generateMessage?key={API_KEY}"
    json_request_body = {
        "prompt": {
            "context": f"{os.getenv('CONTEXT')}",
            "examples": json.load(open("examples.json")),
            "messages": [{"content": f"{get_prompt()}"}],
        },
        "temperature": float(os.getenv("TEMPERATURE")),
        "candidate_count": int(os.getenv("CANDIDATE_COUNT")),
        "topP": float(os.getenv("TOP-P")),
        "topK": int(os.getenv("TOP-K")),
    }
    response = requests.post(api_url, json=json_request_body)
    print(json.dumps(response.json(), indent=2))

    main()


def get_prompt():
    print("Type a prompt:")
    return input()


if __name__ == "__main__":
    main()
