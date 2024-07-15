import os
import json
import requests
from dotenv import load_dotenv

def login():
    url = "https://prod.studysmarter.de/api-token-auth/"

    payload = json.dumps({
    "username": os.getenv('EMAIL'),
    "password": os.getenv('PASS'),
    "platform": "webapp",
    "amplitude_device_id": "mIV1uiiaA0UvvAPUZjnZx6"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["token"]

def add_cart(token, s_id, data):
    print(token, s_id, data)
    url = f"https://prod.studysmarter.de/studysets/{s_id}/flashcards/"

    payload = json.dumps({
        "flashcard_image_ids": [],
        "tags": [],
        "question_html": [
            {
            "text": f"<p>{data["question"]}</p>",
            "is_correct": True
            }
        ],
        "answer_html": [
            {
            "text": f"<p>{data["answer"]}</p>",
            "is_correct": True
            }
        ],
        "shared": 2,
        "hint_html": [],
        "solution_html": ""
    })
    headers = {
        'Content-Type': 'application/json',
        'authorization': f"Token {token}",
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

def main(STUDYSET):

    # Log in to Vaia
    token = login()
    print("LOGIN TOKEN: ", token)

    # Load the studyset
    with open(STUDYSET, "r") as f:
        studyset_data = json.load(f)
        
    s_id = studyset_data["studyset"]
    s_data = studyset_data["data"]

    print("STUDYSET ID: ", s_id)

    # Create a studyset
    for data in s_data:
        print("CREATING FLASHCARD FOR QUESTION: ", data["question"])
        add_cart(token, s_id, data)

    pass

if __name__ == "__main__":
    load_dotenv()

    STUDYSET = "studysets/100-words.json"
    main(STUDYSET)
