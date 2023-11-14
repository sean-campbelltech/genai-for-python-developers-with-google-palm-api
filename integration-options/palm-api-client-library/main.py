# Step 1: pip3 install -r requirements.txt
# Step 2: Create .env file and add env variables

from dotenv import load_dotenv
import google.generativeai as palm
import json
import os


def main():
    load_dotenv()

    PALM_API_KEY = os.getenv("PALM_API_KEY")
    MODEL_ID = os.getenv("MODEL_ID")

    palm.configure(api_key=PALM_API_KEY)
    model = palm.get_model(MODEL_ID)
    examples = build_examples()
    reply = palm.chat(
        model=model,
        context=os.getenv("CONTEXT"),
        examples=examples,
        messages=get_prompt(),
        candidate_count=int(os.getenv("CANDIDATE_COUNT")),
        temperature=float(os.getenv("TEMPERATURE")),
        top_p=float(os.getenv("TOP-P")),
        top_k=int(os.getenv("TOP-K")),
    )

    print(reply.last)
    main()


def get_prompt():
    print("Type a prompt:")
    return input()


def build_examples():
    examples_data = json.load(open("examples.json"))
    return [(entry["input"], entry["output"]) for entry in examples_data]


if __name__ == "__main__":
    main()
