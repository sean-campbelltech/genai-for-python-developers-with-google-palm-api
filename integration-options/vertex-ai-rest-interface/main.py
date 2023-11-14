# Step 1: Copy service account JSON key file into application directory
# Step 2: pip3 install -r requirements.txt
# Step 3: Create .env file and add API_ENDPOINT, PROJECT_ID, and MODEL_NAME env variables

from google.oauth2 import service_account
from dotenv import load_dotenv
import google.auth.transport.requests
import requests
import json
import os


def main():
    load_dotenv()

    API_ENDPOINT = os.getenv("API_ENDPOINT")
    LOCATION = os.getenv("LOCATION")
    PUBLISHER = os.getenv("PUBLISHER")
    PROJECT_ID = os.getenv("PROJECT_ID")
    MODEL_ID = os.getenv("MODEL_ID")

    api_url = f"https://{API_ENDPOINT}/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/{PUBLISHER}/models/{MODEL_ID}:predict"
    json_request_body = {"instances": get_instances(), "parameters": get_parameters()}
    access_token = get_access_token()

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(api_url, json=json_request_body, headers=headers)
    print(json.dumps(response.json(), indent=2))

    main()


def get_access_token():
    SERVICE_ACCOUNT_FILE_PATH = os.getenv("SERVICE_ACCOUNT_FILE_PATH")
    SCOPES = os.getenv("SCOPES")

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE_PATH,
        scopes=[SCOPES],
    )
    credentials.refresh(google.auth.transport.requests.Request())
    access_token = credentials.token
    return access_token


def get_parameters():
    return {
        "candidateCount": int(os.getenv("CANDIDATE_COUNT")),
        "maxOutputTokens": int(os.getenv("MAX_OUTPUT_TOKENS")),
        "temperature": float(os.getenv("TEMPERATURE")),
        "topP": float(os.getenv("TOP-P")),
        "topK": int(os.getenv("TOP-K")),
    }


def get_prompt():
    print("Type a prompt:")
    return input()


def get_instances():
    CONTEXT = os.getenv("CONTEXT")
    examples = json.load(open("examples.json"))
    input_output_instances = ""

    for example in examples:
        input_value = example["input"]
        output_value = example["output"]
        input_output_instances += f"input: {input_value}\noutput: {output_value}\n\n"

    content_value = (
        f"{CONTEXT}\n\n{input_output_instances}input: {get_prompt()}\noutput:\n"
    )

    return [{"content": content_value}]


if __name__ == "__main__":
    main()
