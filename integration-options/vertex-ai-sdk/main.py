# Step 1: Copy service account JSON key file into application directory
# Step 2: pip3 install -r requirements.txt
# The error "No module named 'pkg_resources'" occurs when you don't have the setuptools package installed.
# Then if above error -> run: pip3 install --upgrade setuptools
# Step 3: Create .env file and add API_KEY and MODEL_NAME env variables

import vertexai
from google.oauth2 import service_account
from vertexai.language_models import TextGenerationModel
from dotenv import load_dotenv
import json
import os


def main():
    load_dotenv()

    SERVICE_ACCOUNT_FILE_PATH = os.getenv("SERVICE_ACCOUNT_FILE_PATH")
    SCOPES = os.getenv("SCOPES")
    PROJECT_ID = os.getenv("PROJECT_ID")
    LOCATION = os.getenv("LOCATION")
    MODEL_ID = os.getenv("MODEL_ID")

    # First Authenticate
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE_PATH,
        scopes=[SCOPES],
    )
    # Then init vertexai and call text prompt prediction
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
    model = TextGenerationModel.from_pretrained(MODEL_ID)

    response = model.predict(build_prompt(), **get_parameters())
    print(f"Response from Model: {response.text}")

    main()


def get_prompt():
    print("Type a prompt:")
    return input()


def build_prompt():
    CONTEXT = os.getenv("CONTEXT")
    examples = json.load(open("examples.json"))
    input_output_instances = ""

    for example in examples:
        input_value = example["input"]
        output_value = example["output"]
        input_output_instances += f"input: {input_value}\noutput: {output_value}\n\n"

    return f"""{CONTEXT}\n\n{input_output_instances}input: {get_prompt()}\noutput:\n"""


def get_parameters():
    return {
        "candidate_count": int(os.getenv("CANDIDATE_COUNT")),
        "max_output_tokens": int(os.getenv("MAX_OUTPUT_TOKENS")),
        "temperature": float(os.getenv("TEMPERATURE")),
        "top_p": float(os.getenv("TOP-P")),
        "top_k": int(os.getenv("TOP-K")),
    }


if __name__ == "__main__":
    main()
